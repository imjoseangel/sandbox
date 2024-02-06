FROM mcr.microsoft.com/dotnet/sdk:latest

# https://www.nuget.org/packages/dotnet-script/
RUN dotnet tool install --global dotnet-script --version 1.5.0 --tool-path /usr/bin

ENTRYPOINT [ "dotnet", "script" ]
