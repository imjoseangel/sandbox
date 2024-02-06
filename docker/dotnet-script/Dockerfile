FROM mcr.microsoft.com/dotnet/sdk:latest

# https://www.nuget.org/packages/dotnet-script/
RUN dotnet tool install dotnet-script --version 1.5.0 --tool-path /usr/bin

COPY helloworld.csx /app/helloworld.csx
