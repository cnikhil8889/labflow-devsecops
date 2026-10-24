$ErrorActionPreference = 'Stop'
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Python tests failed' }
dotnet build clients/LabFlow.Check --configuration Release
if ($LASTEXITCODE -ne 0) { throw '.NET build failed' }
