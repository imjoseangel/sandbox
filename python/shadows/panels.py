from dataclasses import dataclass
from typing import Dict, List
import logging

from pvlib import solarposition
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
import pandas as pd
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LATITUDE = 40.4167
LONGITUDE = -3.7033
TIMEZONE = 'Europe/Madrid'

ROOF_BEARING = 40.0  # Updated to 40° NE based on new measurements


@dataclass
class RoofConfig:
    area: float = 75.0  # m²
    width: float = 7.0  # m
    bearing: float = ROOF_BEARING  # roof orientation relative to true North

    @property
    def length(self) -> float:
        return self.area / self.width


@dataclass
class PanelConfig:
    width: float = 1.134  # m (1134mm)
    height: float = 2.094  # m (2094mm)
    thickness: float = 0.035  # m (35mm)
    tilt: float = 20.0  # degrees
    azimuth: float = 180.0 + ROOF_BEARING  # facing south + roof bearing correction
    rear_height: float = 0.40  # m above roof
    front_height: float = 0.12  # m above roof
    rows: int = 2
    columns: int = 5

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def count(self) -> int:
        return self.rows * self.columns


@dataclass
class ChimneyConfig:
    width: float = 1.00  # m (100cm width)
    height: float = 1.10  # m (110cm height)
    depth: float = 0.50  # m (50cm depth)
    position_offset_x: float = 1.0  # m from panels
    position_offset_y: float = -0.5  # m from bottom row


class SolarPanelShadowAnalyzer:
    def __init__(self, lat: float, lon: float, tz: str):
        self.latitude = lat
        self.longitude = lon
        self.timezone = tz

        # Initialize configurations
        self.roof = RoofConfig()
        self.panel_config = PanelConfig()
        self.chimney_config = ChimneyConfig()

        # Calculate layout with compass correction
        self.panels = self._calculate_panel_layout()
        self.chimney = self._calculate_chimney_position()

        self._print_specifications()

    def _calculate_panel_layout(self) -> Dict[str, Dict[str, float]]:
        """Calculate positions for all panels."""
        config = self.panel_config
        roof = self.roof

        # Calculate spacing
        total_width = config.columns * config.width
        column_spacing = (roof.width - total_width) / (config.columns + 1)

        total_height = config.rows * config.height
        row_spacing = (roof.length - total_height) / 3

        # Starting positions
        start_x = -roof.width / 2 + column_spacing + config.width / 2
        start_y_top = roof.length / 2 - row_spacing - config.height / 2
        start_y_bottom = start_y_top - config.height - row_spacing

        panels = {}

        # Top row panels
        top_labels = ['top_left', 'top_left_center',
                      'top_center', 'top_right_center', 'top_right']
        for i, label in enumerate(top_labels):
            panels[label] = {
                'x': start_x + i * (config.width + column_spacing),
                'y': start_y_top,
                'width': config.width,
                'height': config.height
            }

        # Bottom row panels
        bottom_labels = ['bottom_left', 'bottom_left_center',
                         'bottom_center', 'bottom_right_center', 'bottom_right']
        for i, label in enumerate(bottom_labels):
            panels[label] = {
                'x': start_x + i * (config.width + column_spacing),
                'y': start_y_bottom,
                'width': config.width,
                'height': config.height
            }

        return panels

    def _calculate_chimney_position(self) -> Dict[str, float]:
        """Calculate chimney position relative to panels."""
        # Position chimney east of rightmost panels
        rightmost_panel_x = max(panel['x'] for panel in self.panels.values())

        return {
            'x': rightmost_panel_x + self.panel_config.width / 2 +
            self.chimney_config.position_offset_x,
            'y': self.panels['bottom_right']['y'] + self.chimney_config.position_offset_y,
            'width': self.chimney_config.width,
            'height': self.chimney_config.height,
            'depth': self.chimney_config.depth,
            'effective_height': self.chimney_config.height + self.panel_config.rear_height
        }

    def _print_specifications(self) -> None:
        """Print system specifications with compass correction."""
        logger.info("=== ROOF SPECIFICATIONS (COMPASS CORRECTED) ===")
        logger.info(f"Roof area: {self.roof.area} m²")
        logger.info(
            f"Roof dimensions: {self.roof.width}m × {self.roof.length:.2f}m")
        logger.info(f"Roof bearing: {self.roof.bearing}° from True North")
        logger.info(f"Top edge direction: {self.roof.bearing}°N")
        logger.info(
            f"Bottom edge direction: {(self.roof.bearing + 180) % 360}°N")
        logger.info(
            "Location: Cabanillas del Campo, Guadalajara (680m elevation)")

        logger.info("\n=== PANEL SPECIFICATIONS ===")
        logger.info(f"Panel azimuth (corrected): {self.panel_config.azimuth}°")
        logger.info(f"Panel count: {self.panel_config.count}")
        logger.info(
            f"Total panel area: {self.panel_config.count * self.panel_config.area:.1f}m²")

    def calculate_sun_position(self, date_range: List[str]) -> pd.DataFrame:
        """Calculate sun position for given date range."""
        times = pd.date_range(
            start=date_range[0],
            end=date_range[1],
            freq='15min',
            tz=self.timezone
        )
        result = solarposition.get_solarposition(
            times, self.latitude, self.longitude)
        # Ensure we always return a DataFrame
        if isinstance(result, np.ndarray):
            return pd.DataFrame(result, index=times)
        return result

    def calculate_shadow_length(self, sun_elevation: float, object_height: float) -> float:
        """Calculate shadow length based on sun elevation and object height."""
        if sun_elevation <= 0:
            return float('inf')
        return object_height / np.tan(np.radians(sun_elevation))

    def calculate_shadow_coordinates(self,
                                     sun_azimuth: float,
                                     sun_elevation: float) -> Dict[str, float]:
        """Calculate shadow coordinates with compass correction."""
        shadow_length = self.calculate_shadow_length(
            sun_elevation, self.chimney['effective_height'])

        # CORRECTED: Apply roof bearing to shadow calculations
        # Shadow azimuth is opposite to sun azimuth
        shadow_azimuth = (sun_azimuth + 180) % 360

        # Convert to roof coordinate system (bearing-corrected)
        # Roof coordinate system: positive Y = toward roof bearing (11°N)
        roof_relative_azimuth = (shadow_azimuth - self.roof.bearing) % 360
        shadow_azimuth_rad = np.radians(roof_relative_azimuth)

        # Calculate shadow end position in roof coordinates
        # X: positive = toward (11° + 90°) = 101°N
        # Y: positive = toward 11°N
        shadow_end_x = self.chimney['x'] + \
            shadow_length * np.sin(shadow_azimuth_rad)
        shadow_end_y = self.chimney['y'] + \
            shadow_length * np.cos(shadow_azimuth_rad)

        return {
            'start_x': self.chimney['x'],
            'start_y': self.chimney['y'],
            'end_x': shadow_end_x,
            'end_y': shadow_end_y,
            'length': shadow_length,
            'azimuth': shadow_azimuth,
            'roof_relative_azimuth': roof_relative_azimuth,
            'true_azimuth': sun_azimuth
        }

    def check_panel_shading(self,
                            shadow_coords: Dict[str, float],
                            panel_coords: Dict[str, float]) -> bool:
        """Check if shadow intersects with a panel."""
        if shadow_coords['length'] < 0.5:
            return False

        # Panel boundaries
        panel_bounds = {
            'left': panel_coords['x'] - panel_coords['width'] / 2,
            'right': panel_coords['x'] + panel_coords['width'] / 2,
            'bottom': panel_coords['y'] - panel_coords['height'] / 2,
            'top': panel_coords['y'] + panel_coords['height'] / 2
        }

        # Check distance to panel center
        distances = [
            abs(shadow_coords['end_x'] - panel_coords['x']) +
            abs(shadow_coords['end_y'] - panel_coords['y']),
            abs(shadow_coords['start_x'] - panel_coords['x']) +
            abs(shadow_coords['start_y'] - panel_coords['y'])
        ]

        if min(distances) < 2.0:
            return True

        # Line-rectangle intersection check
        if shadow_coords['start_x'] != shadow_coords['end_x']:
            for y in [panel_bounds['bottom'], panel_bounds['top']]:
                y_range = [shadow_coords['start_y'], shadow_coords['end_y']]
                if min(y_range) <= y <= max(y_range):
                    t = (y - shadow_coords['start_y']) / \
                        (shadow_coords['end_y'] - shadow_coords['start_y'])
                    x_intersect = shadow_coords['start_x'] + t * \
                        (shadow_coords['end_x'] - shadow_coords['start_x'])
                    if panel_bounds['left'] <= x_intersect <= panel_bounds['right']:
                        return True

        return False

    def analyze_monthly_shadows(self) -> Dict[int, pd.DataFrame]:
        """Analyze shadows for each month of the year."""
        results = {}

        for month in range(1, 13):
            date_range = [f"2024-{month:02d}-15 00:00:00",
                          f"2024-{month:02d}-15 23:59:59"]
            solar_pos = self.calculate_sun_position(date_range)

            monthly_data = []
            time_index = []

            for time, row in solar_pos.iterrows():
                if row['elevation'] > 0:
                    shadow = self.calculate_shadow_coordinates(
                        row['azimuth'], row['elevation'])
                    is_shaded = self.check_panel_shading(
                        shadow, self.panels['bottom_right'])

                    monthly_data.append({
                        'elevation': row['elevation'],
                        'azimuth': row['azimuth'],
                        'shadow_length': shadow['length'],
                        'bottom_right_shaded': is_shaded
                    })
                    time_index.append(time)

            if monthly_data:
                results[month] = pd.DataFrame(monthly_data, index=time_index)
                logger.info(
                    f"Month {month}: {len(monthly_data)} daylight data points")

        return results

    def _plot_solar_path(self, ax: Axes, solar_pos: pd.DataFrame, month: int) -> None:
        """Plot solar path for the month."""
        daylight_pos = solar_pos[solar_pos['elevation'] > 0]
        ax.plot(daylight_pos['azimuth'], daylight_pos['elevation'])
        ax.set_xlabel('Solar Azimuth (degrees)')
        ax.set_ylabel('Solar Elevation (degrees)')
        ax.set_title(f'Solar Path - Month {month}')
        ax.grid(True)

    def _plot_shadow_length(self, ax: Axes, solar_pos: pd.DataFrame, month: int) -> None:
        """Plot shadow length throughout the day."""
        shadow_data = []
        times = []

        for time, row in solar_pos.iterrows():
            if row['elevation'] > 0:
                shadow_length = min(self.calculate_shadow_length(
                    row['elevation'], self.chimney['height']), 20)
                shadow_data.append(shadow_length)
                times.append(time.hour + time.minute / 60)

        if times:
            ax.plot(times, shadow_data)
            ax.set_xlabel('Time of Day (hours)')
            ax.set_ylabel('Shadow Length (m)')
            ax.set_title(f'Shadow Length Throughout Day - Month {month}')
            ax.grid(True)

    def _draw_roof_and_panels(self, ax: Axes) -> float:
        """Draw roof outline and all panels with compass-corrected labels."""
        # Draw roof
        roof_rect = patches.Rectangle(
            (-self.roof.width / 2, -self.roof.length / 2),
            self.roof.width, self.roof.length,
            linewidth=2, edgecolor='gray', facecolor='lightgray', alpha=0.3
        )
        ax.add_patch(roof_rect)

        # Panel labels
        panel_labels = {
            'top_left': 'T1', 'top_left_center': 'T2', 'top_center': 'T3',
            'top_right_center': 'T4', 'top_right': 'T5',
            'bottom_left': 'B1', 'bottom_left_center': 'B2', 'bottom_center': 'B3',
            'bottom_right_center': 'B4', 'bottom_right': 'B5\n(AFFECTED)'
        }

        total_area = 0.0
        for panel_name, panel in self.panels.items():
            total_area += panel['width'] * panel['height']

            # Highlight affected panel
            if panel_name == 'bottom_right':
                color, edge_color, linewidth = 'lightcoral', 'red', 3
            else:
                color, edge_color, linewidth = 'lightblue', 'blue', 1

            rect = patches.Rectangle(
                (panel['x'] - panel['width'] / 2,
                 panel['y'] - panel['height'] / 2),
                panel['width'], panel['height'],
                linewidth=linewidth, edgecolor=edge_color, facecolor=color, alpha=0.8
            )
            ax.add_patch(rect)
            ax.text(panel['x'], panel['y'], panel_labels[panel_name],
                    ha='center', va='center', fontsize=9, fontweight='bold')

        return total_area

    def _draw_chimney(self, ax: Axes) -> None:
        """Draw chimney on the plot."""
        chimney_rect = patches.Rectangle(
            (self.chimney['x'] - self.chimney['width'] / 2,
             self.chimney['y'] - self.chimney['depth'] / 2),
            self.chimney['width'], self.chimney['depth'],
            linewidth=3, edgecolor='darkred', facecolor='red', alpha=0.9
        )
        ax.add_patch(chimney_rect)

        ax.text(self.chimney['x'], self.chimney['y'],
                f"(CHIMNEY\n{self.chimney['width'] * 100:.0f}x"
                f"{self.chimney_config.depth * 100:.0f}cm\n)"
                f"H:{self.chimney['height'] * 100:.0f}cm",
                ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    def _draw_shadows(self, ax: Axes, solar_pos: pd.DataFrame) -> None:
        """Draw shadows at key times."""
        key_hours = [10, 11, 12, 13]
        colors = ['orange', 'purple', 'green', 'blue']
        labels = ['10:00', '11:00', '12:00', '13:00']

        for i, hour in enumerate(key_hours):
            target_times = solar_pos.index[(solar_pos.index.hour == hour) &
                                           (abs(solar_pos.index.minute) <= 7)]
            if len(target_times) > 0:
                row = solar_pos.loc[target_times[0]]
                if row['elevation'] > 0:
                    shadow = self.calculate_shadow_coordinates(
                        row['azimuth'], row['elevation'])

                    ax.plot([shadow['start_x'], shadow['end_x']],
                            [shadow['start_y'], shadow['end_y']],
                            color=colors[i], linewidth=4, alpha=0.8,
                            label=f"({labels[i]} (Az:{row['azimuth']:.0f}°, "
                            f"El:{row['elevation']:.0f}°))")

                    ax.text(shadow['end_x'], shadow['end_y'], f'{shadow["length"]:.1f}m',
                            fontsize=8, color=colors[i], fontweight='bold')

        ax.legend(loc='upper left', fontsize=8)

    def plot_shadow_analysis(self, month: int = 6) -> None:
        """Plot comprehensive shadow analysis for a specific month."""
        _, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

        # Calculate solar position
        date_range = [f"2024-{month:02d}-15 00:00:00",
                      f"2024-{month:02d}-15 23:59:59"]
        solar_pos = self.calculate_sun_position(date_range)

        # Plot 1: Solar path
        self._plot_solar_path(ax1, solar_pos, month)

        # Plot 2: Shadow length
        self._plot_shadow_length(ax2, solar_pos, month)

        # Plot 3: Panel layout with shadows
        ax3.set_aspect('equal')
        total_area = self._draw_roof_and_panels(ax3)
        self._draw_chimney(ax3)
        self._draw_shadows(ax3, solar_pos)

        # Add compass directions with CORRECTED bearings
        ax3.text(0, self.roof.length / 2 - 1, f'{self.roof.bearing:.0f}°N',
                 ha='center', va='center', fontsize=16, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
        ax3.text(0, -self.roof.length / 2 + 1, f'{(self.roof.bearing + 180) % 360:.0f}°N',
                 ha='center', va='center', fontsize=16, fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))

        # Set plot limits and labels with corrected compass directions
        margin = 1.5
        ax3.set_xlim(-self.roof.width / 2 - margin,
                     self.roof.width / 2 + margin + 2)
        ax3.set_ylim(-self.roof.length / 2 - margin,
                     self.roof.length / 2 + margin)

        # CORRECTED: Labels based on actual compass bearing
        east_bearing = (self.roof.bearing + 90) % 360
        west_bearing = (self.roof.bearing + 270) % 360
        ax3.set_xlabel(f'{west_bearing:.0f}°N ← → {east_bearing:.0f}°N')
        ax3.set_ylabel(
            f'{(self.roof.bearing + 180) % 360:.0f}°N ← → {self.roof.bearing:.0f}°N')
        ax3.set_title(f"Solar Panel Layout - Month {month} (Roof Bearing: {self.roof.bearing}°N)\n"
                      f"Total Area: {total_area:.1f}m² \
                        ({total_area / self.roof.area * 100:.1f}% coverage)")

        # Plot 4: Monthly shading analysis
        self._plot_monthly_shading(ax4)

        plt.tight_layout()
        plt.show()

    def _plot_monthly_shading(self, ax: Axes) -> None:
        """Plot monthly shading percentages."""
        monthly_results = self.analyze_monthly_shadows()
        months = list(range(1, 13))
        shading_percentages = []

        for month in months:
            if month in monthly_results:
                df = monthly_results[month]
                if len(df) > 0:
                    total_hours = len(df)
                    shaded_hours = df['bottom_right_shaded'].sum()
                    percentage = (shaded_hours / total_hours) * 100
                    shading_percentages.append(percentage)
                else:
                    shading_percentages.append(0)
            else:
                shading_percentages.append(0)

        ax.bar(months, shading_percentages, color='red', alpha=0.7)
        ax.set_xlabel('Month')
        ax.set_ylabel('Shading Percentage (%)')
        ax.set_title('Bottom Right Panel (B5) - Shading Throughout Year')
        ax.set_xticks(months)
        ax.grid(True, alpha=0.3)

    def generate_hourly_shading_report(self) -> None:
        """Generate detailed hourly shading heatmap."""
        monthly_results = self.analyze_monthly_shadows()

        hours = list(range(6, 19))
        months = list(range(1, 13))
        heatmap_data = np.zeros((len(months), len(hours)))

        for i, month in enumerate(months):
            if month in monthly_results:
                df = monthly_results[month]
                for j, hour in enumerate(hours):
                    hour_data = df[df.index.hour == hour]
                    if len(hour_data) > 0:
                        heatmap_data[i,
                                     j] = hour_data['bottom_right_shaded'].mean()

        plt.figure(figsize=(12, 8))
        sns.heatmap(heatmap_data,
                    xticklabels=[f"{h}:00" for h in hours],
                    yticklabels=[f"Month {m}" for m in months],
                    cmap='Reds', annot=True, fmt='.2f',
                    cbar_kws={'label': 'Shading Probability'})

        plt.title('Bottom Right Panel (B5) - Shading Probability Throughout Year')
        plt.xlabel('Hour of Day')
        plt.ylabel('Month')
        plt.tight_layout()
        plt.show()

    def generate_summary_report(self) -> None:
        """Generate comprehensive analysis report."""
        monthly_results = self.analyze_monthly_shadows()

        logger.info("\n=== SHADOW ANALYSIS RESULTS ===")
        logger.info("Real observation: B5 panel shaded 9:15-13:30 on Sep 23rd")

        for month in range(1, 13):
            if month in monthly_results:
                df = monthly_results[month]
                if len(df) > 0:
                    shaded_times = df[df['bottom_right_shaded']]
                    if len(shaded_times) > 0:
                        first_shade = shaded_times.index.min().strftime("%H:%M")
                        last_shade = shaded_times.index.max().strftime("%H:%M")
                        percentage = (len(shaded_times) / len(df)) * 100

                        logger.info(
                            f"(Month {month:2d}: B5 shaded "
                            f"{first_shade}-{last_shade} ({percentage:.1f}%))")

                        if month == 9:  # September validation
                            morning_shade = df[(df.index.to_series().dt.hour >= 9) &
                                               (df.index.to_series().dt.hour <= 14) &
                                               (df['bottom_right_shaded'])]
                            if len(morning_shade) > 0:
                                real_first = morning_shade.index.min().strftime("%H:%M")
                                real_last = morning_shade.index.max().strftime("%H:%M")
                                logger.info(
                                    f"(Morning period: {real_first}-{real_last} "
                                    f"(vs real 9:15-13:30))")
                    else:
                        logger.info(f"Month {month:2d}: No shading detected")


def main():
    """Main execution function with compass correction validation."""
    # Create analyzer
    analyzer = SolarPanelShadowAnalyzer(LATITUDE, LONGITUDE, TIMEZONE)

    logger.info(f"Analyzing shadows for location: {LATITUDE}, {LONGITUDE}")
    logger.info(
        f"Compass correction applied: Roof bearing {ROOF_BEARING}° from True North")
    logger.info(
        "Location: Cabanillas del Campo, Guadalajara, Spain (680m elevation)")

    # COMPASS VALIDATION SECTION - UPDATED FOR 40° NE
    print("\n=== COMPASS ALIGNMENT VALIDATION (UPDATED TO 40° NE) ===")
    print(f"Compass reading from image: {ROOF_BEARING}°N at top of roof")
    print(f"GPS coordinates: {LATITUDE}°N, {abs(LONGITUDE)}°W")
    print("Location: Cabanillas del Campo, Guadalajara, Spain")
    print("Elevation: 680m above sea level")
    print(
        f"Corrected panel azimuth: {analyzer.panel_config.azimuth}° (facing south + roof bearing)")

    print("\n=== CORRECTED DIRECTIONAL REFERENCES (40° NE) ===")
    print(f"Top edge (toward): {ROOF_BEARING}°N")
    print(f"Bottom edge (toward): {(ROOF_BEARING + 180) % 360}°N")
    print(
        f"Right edge (toward): {(ROOF_BEARING + 90) % 360}°N (East relative to roof)")
    print(
        f"Left edge (toward): {(ROOF_BEARING + 270) % 360}°N (West relative to roof)")
    print("Chimney position: Right side (East relative to roof)")
    print("Affected panel: B5 (bottom-right)")

    # SHADOW CALIBRATION BASED ON REAL MEASUREMENT
    print("\n=== SHADOW CALIBRATION & CHIMNEY DIMENSIONS ===")
    print("Real measurement: 20cm object → 30cm shadow")
    print("Estimated Chimney Dimensions:")
    print(f"  Height: {analyzer.chimney_config.height * 100:.0f}cm")
    print(f"  Width: {analyzer.chimney_config.width * 100:.0f}cm")
    print(f"  Depth: {analyzer.chimney_config.depth * 100:.0f}cm")
    print(
        f"  Effective height (including panel): {analyzer.chimney['effective_height'] * 100:.0f}cm")

    # Verify calibration with today's measurement
    calibration_date = "2024-09-24 11:30:00"
    solar_pos = analyzer.calculate_sun_position(
        [calibration_date, calibration_date])

    if len(solar_pos) > 0:
        row = solar_pos.iloc[0]
        # Calculate what shadow a 20cm object would cast
        test_shadow_length = analyzer.calculate_shadow_length(
            row['elevation'], 0.20)
        print(
            f"Predicted shadow for 20cm object: {test_shadow_length * 100:.0f}cm")
        print("Actual measured shadow: 30cm")
        print(f"Sun elevation at 11:30am: {row['elevation']:.1f}°")
        print(f"Sun azimuth at 11:30am: {row['azimuth']:.1f}°")

    # Re-run shadow analysis with compass correction
    print("\n=== COMPASS-CORRECTED SHADOW ANALYSIS (40° NE) ===")
    print("Testing September 23rd shading (real observation: 9:15-13:30)")

    test_date = "2024-09-23"
    test_times = ["09:15", "11:00", "13:30"]

    for test_time in test_times:
        test_datetime = f"{test_date} {test_time}:00"
        solar_pos = analyzer.calculate_sun_position(
            [test_datetime, test_datetime])

        if len(solar_pos) > 0:
            row = solar_pos.iloc[0]
            shadow = analyzer.calculate_shadow_coordinates(
                row['azimuth'], row['elevation']
            )

            is_shaded = analyzer.check_panel_shading(
                shadow, analyzer.panels['bottom_right']
            )

            print(f"\n{test_time} on Sep 23rd:")
            print(
                f"  True sun azimuth: {row['azimuth']:.1f}° (from True North)")
            print(f"  Sun elevation: {row['elevation']:.1f}°")
            print(f"  Shadow azimuth (true): {shadow['azimuth']:.1f}°")
            print(
                f"  Shadow azimuth (roof-relative): {shadow['roof_relative_azimuth']:.1f}°")
            print(f"  Shadow length: {shadow['length']:.2f}m")
            print(
                f"  Shadow end position: ({shadow['end_x']:.1f}, {shadow['end_y']:.1f})")
            print(
                f"  B5 panel position: ({analyzer.panels['bottom_right']['x']:.1f}, "
                f"{analyzer.panels['bottom_right']['y']:.1f})")
            print(f"  B5 panel shaded: {is_shaded}")

            if is_shaded:
                print("  ✓ Model predicts shading - MATCHES observation")
            else:
                print("  ✗ Model shows no shading - needs calibration")

            # Check shadow direction relative to chimney-to-panel vector
            chimney_to_panel_x = analyzer.panels['bottom_right']['x'] - \
                analyzer.chimney['x']
            chimney_to_panel_y = analyzer.panels['bottom_right']['y'] - \
                analyzer.chimney['y']
            shadow_vector_x = shadow['end_x'] - shadow['start_x']
            shadow_vector_y = shadow['end_y'] - shadow['start_y']

            # Dot product to check if shadow points toward panel
            dot_product = chimney_to_panel_x * shadow_vector_x + \
                chimney_to_panel_y * shadow_vector_y
            shadow_toward_panel = dot_product > 0

            print(f"  Shadow pointing toward B5: {shadow_toward_panel}")

    # Generate seasonal analyses
    seasons = [(3, "Spring"), (6, "Summer"), (9, "Fall"), (12, "Winter")]
    for month, season in seasons:
        logger.info(f"\nAnalyzing {season} (Month {month})...")
        analyzer.plot_shadow_analysis(month)

    # Generate reports
    logger.info("\nGenerating yearly heatmap...")
    analyzer.generate_hourly_shading_report()

    analyzer.generate_summary_report()


if __name__ == "__main__":
    main()
