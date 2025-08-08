def CustomCSS() -> str:
    """Returns the custom CSS for the agent."""

    _CUSTOM_CSS = """
        /* Respect Gradio's native dark/light mode */
        .dark {
            background: #0f0f0f !important;
            color: #e8eaed !important;
        }

        .light {
            background: #ffffff !important;
            color: #202124 !important;
        }

        /* Show footer with appropriate styling */
        footer {
            display: none !important;
            background: transparent !important;
            border: none !important;
        }

        .dark footer {
            color: #999 !important;
        }

        .light footer {
            color: #666 !important;
        }

        /* Header logo section */
        .header-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid transparent;
        }

        /* Logo container */
        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 70px;
        }

        .logo-circle {
            width: 50px;
            height: 50px;
            background: transparent;
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            position: relative;
            overflow: hidden;
        }

        .logo-shine {
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent 30%, rgba(102, 126, 234, 0.1) 50%, transparent 70%);
            animation: shine 3s ease-in-out infinite;
        }

        .logo-icon {
            position: relative;
            z-index: 1;
        }

        @keyframes shine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            50% { transform: translateX(100%) translateY(100%) rotate(45deg); }
            100% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        }

        /* Header welcome section */
        .header-welcome {
            display: flex;
            flex-direction: column;
            justify-content: center;
            height: 70px;
            padding-left: 20px;
        }

        .header-title {
            margin: 0 0 4px 0;
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header-subtitle {
            margin: 0;
            color: #64748b;
            font-size: 14px;
            font-weight: 500;
        }

        .dark .header-logo {
            background: #1e1e1e !important;
            border-color: #333 !important;
        }

        .light .header-logo {
            background: #f8f9fa !important;
            border-color: #e8eaed !important;
        }

        /* Theme-specific logo circle styles */
        .dark .logo-circle {
            border-color: rgba(102, 126, 234, 0.4) !important;
        }

        .light .logo-circle {
            border-color: rgba(102, 126, 234, 0.3) !important;
        }

        /* Theme-specific header subtitle */
        .dark .header-subtitle {
            color: #9aa0a6 !important;
        }

        .light .header-subtitle {
            color: #64748b !important;
        }

        /* Header welcome section */
        .header-welcome {
            padding: 24px;
            border-radius: 12px;
            border: 1px solid transparent;
        }

        .dark .header-welcome {
            background: #1e1e1e !important;
            border-color: #333 !important;
        }

        .light .header-welcome {
            background: #f8f9fa !important;
            border-color: #e8eaed !important;
        }

        /* Subtle logo watermark */
        .gradio-container::after {
            content: '';
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 120px;
            height: 48px;
            background-image: url('/gradio_api/file=assets/logo.png');
            background-repeat: no-repeat;
            background-size: contain;
            opacity: 0.08;
            pointer-events: none;
            z-index: 1;
        }

        /* Chat window - adapts to theme */
        .dark #chatbot {
            border: 1px solid #333 !important;
            border-radius: 16px !important;
            box-shadow: none !important;
            background-color: #1e1e1e !important;
            overflow: hidden;
        }

        .light #chatbot {
            border: 1px solid #e8eaed !important;
            border-radius: 16px !important;
            box-shadow: none !important;
            background-color: #ffffff !important;
            overflow: hidden;
        }

        /* Global rounded corners for all input fields and containers */
        #chatbot,
        #chat_input,
        .gr-textbox,
        .gr-button,
        .gr-form,
        .gr-box {
            border-radius: 16px !important;
        }

        /* Ensure all gradio components have rounded corners */
        .gradio-container .gr-textbox,
        .gradio-container .gr-button,
        .gradio-container .gr-form,
        .gradio-container .gr-box,
        .gradio-container .multimodal-textbox {
            border-radius: 16px !important;
        }

        /* Hide unnecessary elements */
        #chatbot .icon-button-wrapper.top-panel,
        #chatbot .progress-text {
            display: none !important;
        }

        /* Chat text size */
        #chatbot .message,
        #chatbot .bot,
        #chatbot .user,
        #chatbot p,
        #chatbot div,
        #chatbot span,
        #chatbot * {
            font-size: 14px !important;
            line-height: 1.5 !important;
        }

        /* User messages - Dark mode */
        .dark #chatbot .message.user,
        .dark #chatbot .user {
            background-color: #2f2f2f !important;
            color: #e8eaed !important;
            border-radius: 18px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: none !important;
            border: none !important;
            max-width: 80% !important;
            margin-left: auto !important;
        }

        .dark #chatbot .message.user p,
        .dark #chatbot .user p {
            color: #e8eaed !important;
            margin: 0 !important;
        }

        /* User messages - Light mode */
        .light #chatbot .message.user,
        .light #chatbot .user {
            background-color: #f1f3f4 !important;
            color: #202124 !important;
            border-radius: 18px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            box-shadow: none !important;
            border: none !important;
            max-width: 80% !important;
            margin-left: auto !important;
        }

        .light #chatbot .message.user p,
        .light #chatbot .user p {
            color: #202124 !important;
            margin: 0 !important;
        }

        /* Bot messages - Dark mode */
        .dark #chatbot .message.bot,
        .dark #chatbot .bot {
            background-color: transparent !important;
            color: #e8eaed !important;
            border-radius: 18px !important;
            padding: 12px 0 !important;
            margin: 8px 0 !important;
            box-shadow: none !important;
            border: none !important;
            max-width: 80% !important;
            margin-right: auto !important;
        }

        .dark #chatbot .message.bot p,
        .dark #chatbot .bot p {
            color: #e8eaed !important;
            margin: 0 !important;
        }

        /* Bot messages - Light mode */
        .light #chatbot .message.bot,
        .light #chatbot .bot {
            background-color: transparent !important;
            color: #202124 !important;
            border-radius: 18px !important;
            padding: 12px 0 !important;
            margin: 8px 0 !important;
            box-shadow: none !important;
            border: none !important;
            max-width: 80% !important;
            margin-right: auto !important;
        }

        .light #chatbot .message.bot p,
        .light #chatbot .bot p {
            color: #202124 !important;
            margin: 0 !important;
        }

        /* Custom speech bubble colors - Simple, no gradients */
        #chatbot .message.user,
        #chatbot .user {
            background-color: #D1E9F6 !important; /* Solid soft blue */
            color: #000000 !important;
            border: 1px solid rgba(66, 153, 225, 0.15) !important;
            box-shadow: 0 2px 8px rgba(66, 153, 225, 0.08) !important;
            position: relative !important;
        }

        /* User speech bubble tail (right side) */
        #chatbot .message.user::after,
        #chatbot .user::after {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            right: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-left: 8px solid #D1E9F6 !important;
            border-right: none !important;
        }

        #chatbot .message.user p,
        #chatbot .user p {
            color: #000000 !important;
        }

        #chatbot .message.bot,
        #chatbot .bot {
            background-color: #FED7CC !important; /* Solid soft coral */
            color: #000000 !important;
            padding: 12px 16px !important;
            border: 1px solid rgba(237, 137, 54, 0.15) !important;
            box-shadow: 0 2px 8px rgba(237, 137, 54, 0.08) !important;
            position: relative !important;
        }

        /* Bot speech bubble tail (left side) */
        #chatbot .message.bot::before,
        #chatbot .bot::before {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-right: 8px solid #FED7CC !important;
            border-left: none !important;
        }

        #chatbot .message.bot p,
        #chatbot .bot p {
            color: #000000 !important;
        }

        /* Additional custom classes - simple solids */
        .user_message {
            background-color: #D1E9F6 !important;
            color: #000000 !important;
            border: 1px solid rgba(66, 153, 225, 0.15) !important;
            box-shadow: 0 2px 8px rgba(66, 153, 225, 0.08) !important;
            position: relative !important;
        }

        .user_message::after {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            right: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-left: 8px solid #D1E9F6 !important;
            border-right: none !important;
        }

        .bot_message {
            background-color: #FED7CC !important;
            color: #000000 !important;
            border: 1px solid rgba(237, 137, 54, 0.15) !important;
            box-shadow: 0 2px 8px rgba(237, 137, 54, 0.08) !important;
            position: relative !important;
        }

        .bot_message::before {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-right: 8px solid #FED7CC !important;
            border-left: none !important;
        }

        /* Alternative simple pastel variations (solid) */
        .user_message_mint {
            background-color: #DCFCE7 !important; /* Mint green */
            color: #000000 !important;
            border: 1px solid rgba(34, 197, 94, 0.15) !important;
            box-shadow: 0 2px 8px rgba(34, 197, 94, 0.08) !important;
            position: relative !important;
        }

        .user_message_mint::after {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            right: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-left: 8px solid #DCFCE7 !important;
            border-right: none !important;
        }

        .bot_message_lavender {
            background-color: #E9D5FF !important; /* Lavender */
            color: #000000 !important;
            border: 1px solid rgba(147, 51, 234, 0.15) !important;
            box-shadow: 0 2px 8px rgba(147, 51, 234, 0.08) !important;
            position: relative !important;
        }

        .bot_message_lavender::before {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-right: 8px solid #E9D5FF !important;
            border-left: none !important;
        }

        .user_message_peach {
            background-color: #FEF3C7 !important; /* Soft peach */
            color: #000000 !important;
            border: 1px solid rgba(217, 119, 6, 0.15) !important;
            box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08) !important;
            position: relative !important;
        }

        .user_message_peach::after {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            right: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-left: 8px solid #FEF3C7 !important;
            border-right: none !important;
        }

        .bot_message_sky {
            background-color: #E0F2FE !important; /* Sky blue */
            color: #000000 !important;
            border: 1px solid rgba(14, 165, 233, 0.15) !important;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.08) !important;
            position: relative !important;
        }

        .bot_message_sky::before {
            content: '' !important;
            position: absolute !important;
            top: 50% !important;
            left: -8px !important;
            transform: translateY(-50%) !important;
            width: 0 !important;
            height: 0 !important;
            border: 8px solid transparent !important;
            border-right: 8px solid #E0F2FE !important;
            border-left: none !important;
        }        /* Input field - Dark mode */
        .dark #chat_input {
            border: 1px solid #333 !important;
            border-radius: 24px !important;
            box-shadow: none !important;
            background-color: #2f2f2f !important;
            transition: all 0.2s ease !important;
        }

        .dark #chat_input:hover {
            border-color: #555 !important;
        }

        .dark #chat_input:focus-within {
            border-color: #1a73e8 !important;
            box-shadow: 0 0 0 1px #1a73e8 !important;
        }

        .dark #chat_input textarea,
        .dark #chat_input .multimodal-textbox,
        .dark #chat_input > div,
        .dark #chat_input input,
        .dark #chat_input * {
            background-color: transparent !important;
            color: #e8eaed !important;
            border: none !important;
        }

        /* Input field - Light mode */
        .light #chat_input {
            border: 1px solid #dadce0 !important;
            border-radius: 24px !important;
            box-shadow: none !important;
            background-color: #ffffff !important;
            transition: all 0.2s ease !important;
        }

        .light #chat_input:hover {
            border-color: #bbb !important;
        }

        .light #chat_input:focus-within {
            border-color: #1a73e8 !important;
            box-shadow: 0 0 0 1px #1a73e8 !important;
        }

        .light #chat_input textarea,
        .light #chat_input .multimodal-textbox,
        .light #chat_input > div,
        .light #chat_input input,
        .light #chat_input * {
            background-color: transparent !important;
            color: #202124 !important;
            border: none !important;
        }

        /* Buttons - Dark mode */
        .dark #clear_button,
        .dark #logout_button {
            border: 1px solid #333 !important;
            border-radius: 20px !important;
            box-shadow: none !important;
            background-color: #2f2f2f !important;
            color: #e8eaed !important;
            transition: all 0.2s ease !important;
        }

        /* Special styling for New Chat button */
        #clear_button {
            background: linear-gradient(135deg, #ff6b35, #f7931e) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 20px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3) !important;
        }

        #clear_button:hover {
            background: linear-gradient(135deg, #ff7a45, #ff9e2e) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4) !important;
        }

        .dark #clear_button:hover,
        .dark #logout_button:hover {
            background-color: #3c4043 !important;
            border-color: #555 !important;
        }

        /* Account button stays subtle */
        .dark #logout_button:hover {
            background-color: #3c4043 !important;
            border-color: #555 !important;
        }

        /* Buttons - Light mode */
        .light #clear_button,
        .light #logout_button {
            border: 1px solid #dadce0 !important;
            border-radius: 20px !important;
            box-shadow: none !important;
            background-color: #f8f9fa !important;
            color: #3c4043 !important;
            transition: all 0.2s ease !important;
        }

        /* New Chat button overrides for light mode */
        .light #clear_button {
            background: linear-gradient(135deg, #ff6b35, #f7931e) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3) !important;
        }

        .light #clear_button:hover {
            background: linear-gradient(135deg, #ff7a45, #ff9e2e) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(255, 107, 53, 0.4) !important;
        }

        .light #logout_button:hover {
            background-color: #f1f3f4 !important;
            border-color: #bbb !important;
        }
    """

    return _CUSTOM_CSS


def FooterCSS() -> str:
    """Returns the custom CSS for the footer."""

    _FOOTER_CSS = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
        .imjoseangel-footer {
            color: #999;
            font-size: 12px;
            display: block;
            position: relative;
            width: 100%;
            text-align: center;
            margin-top: 20px;
            font-family: 'Roboto', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        .imjoseangel-footer a {
            color: #e5e5e5;
            text-decoration: none;
            transition: color 0.2s ease;
        }
        .imjoseangel-footer a:hover {
            color: #60a5fa;
        }
        .imjoseangel-footer .fa-heart {
            color: #E90606;
            margin: 0 3px;
            font-size: 10px;
            animation: pound .35s infinite alternate;
            -webkit-animation: pound .35s infinite alternate;
        }
        @-webkit-keyframes pound {
            to {
                transform: scale(1.1);
            }
        }
        @keyframes pound {
            to {
                transform: scale(1.1);
            }
        }
        </style>
        <span class="imjoseangel-footer">
            Made with <i class="fa-solid fa-heart"></i> by
            <a href="#" target="_blank">imjoseangel</a>
        </span>
    """

    return _FOOTER_CSS


def AuthHTML() -> str:
    """Returns the custom HTML for the Auth Screen."""

    _AUTH_HTML = """
        <div style="text-align: center; padding: 40px 20px; font-family: 'Roboto', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div style="margin-bottom: 30px; display: flex; justify-content: center; align-items: center; width: 100%;">
                <img src="/gradio_api/file=assets/logo.png"
                    style="width: auto; height: 80px; max-width: 300px; display: block; margin: 0 auto;"
                    alt="imjoseangel Logo" />
            </div>
            <h2 style="color: #0369a1; margin: 20px 0; font-weight: 500; text-align: center;">
                🤖 AI-Powered Chatbot
            </h2>
            <p style="color: #666; margin-bottom: 30px; font-size: 16px; text-align: center;">
                Please sign in to access your smart assistant
            </p>
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; width: 100%; text-align: center;">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                <style>
                .imjoseangel-auth-footer {
                    color: #666;
                    font-size: 14px;
                    font-family: 'Roboto', sans-serif;
                    -webkit-font-smoothing: antialiased;
                    -moz-osx-font-smoothing: grayscale;
                    text-align: center;
                }
                .imjoseangel-auth-footer a {
                    color: #0369a1;
                    text-decoration: none;
                    font-weight: 500;
                }
                .imjoseangel-auth-footer .fa-heart {
                    color: #E90606;
                    margin: 0 3px;
                    font-size: 12px;
                    animation: pound .35s infinite alternate;
                    -webkit-animation: pound .35s infinite alternate;
                }
                h2.svelte-1ogxbi0 {
                    display: none !important;
                }
                @-webkit-keyframes pound {
                    to {
                        transform: scale(1.1);
                    }
                }
                @keyframes pound {
                    to {
                        transform: scale(1.1);
                    }
                }
                </style>
                <span class="imjoseangel-auth-footer">
                    Made with <i class="fa-solid fa-heart"></i> by
                    <a href="#" target="_blank">imjoseangel</a>
                </span>
            </div>
        </div>
    """

    return _AUTH_HTML
