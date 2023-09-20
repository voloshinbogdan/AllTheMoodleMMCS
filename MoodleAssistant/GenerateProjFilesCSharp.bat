@echo off

goto:begin

:CreateProjBegin
echo ^<^?xml version="1.0" encoding="utf-8"^?^> >> "test.csproj"
echo ^<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003"^> >> "test.csproj"
echo   ^<Import Project="$(MSBuildExtensionsPath)\$(MSBuildToolsVersion)\Microsoft.Common.props" Condition="Exists('$(MSBuildExtensionsPath)\$(MSBuildToolsVersion)\Microsoft.Common.props')" /^> >> "test.csproj"
echo   ^<PropertyGroup^> >> "test.csproj"
echo     ^<Configuration Condition=" '$(Configuration)' == '' "^>Debug^</Configuration^> >> "test.csproj"
echo     ^<Platform Condition=" '$(Platform)' == '' "^>AnyCPU^</Platform^> >> "test.csproj"
echo     ^<ProjectGuid^>{1B7D2050-B86D-485E-8055-4C467CEEEBF2}^</ProjectGuid^> >> "test.csproj"
echo     ^<OutputType^>Exe^</OutputType^> >> "test.csproj"
echo     ^<RootNamespace^>Test^</RootNamespace^> >> "test.csproj"
echo     ^<AssemblyName^>Test^</AssemblyName^> >> "test.csproj"
echo     ^<TargetFrameworkVersion^>v4.7.2^</TargetFrameworkVersion^> >> "test.csproj"
echo     ^<FileAlignment^>512^</FileAlignment^> >> "test.csproj"
echo     ^<AutoGenerateBindingRedirects^>true^</AutoGenerateBindingRedirects^> >> "test.csproj"
echo     ^<Deterministic^>true^</Deterministic^> >> "test.csproj"
echo   ^</PropertyGroup^> >> "test.csproj"
echo   ^<PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Debug|AnyCPU' "^> >> "test.csproj"
echo     ^<PlatformTarget^>AnyCPU^</PlatformTarget^> >> "test.csproj"
echo     ^<DebugSymbols^>true^</DebugSymbols^> >> "test.csproj"
echo     ^<DebugType^>full^</DebugType^> >> "test.csproj"
echo     ^<Optimize^>false^</Optimize^> >> "test.csproj"
echo     ^<OutputPath^>bin\Debug\^</OutputPath^> >> "test.csproj"
echo     ^<DefineConstants^>DEBUG;TRACE^</DefineConstants^> >> "test.csproj"
echo     ^<ErrorReport^>prompt^</ErrorReport^> >> "test.csproj"
echo     ^<WarningLevel^>4^</WarningLevel^> >> "test.csproj"
echo   ^</PropertyGroup^> >> "test.csproj"
echo   ^<PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Release|AnyCPU' "^> >> "test.csproj"
echo     ^<PlatformTarget^>AnyCPU^</PlatformTarget^> >> "test.csproj"
echo     ^<DebugType^>pdbonly^</DebugType^> >> "test.csproj"
echo     ^<Optimize^>true^</Optimize^> >> "test.csproj"
echo     ^<OutputPath^>bin\Release\^</OutputPath^> >> "test.csproj"
echo     ^<DefineConstants^>TRACE^</DefineConstants^> >> "test.csproj"
echo     ^<ErrorReport^>prompt^</ErrorReport^> >> "test.csproj"
echo     ^<WarningLevel^>4^</WarningLevel^> >> "test.csproj"
echo   ^</PropertyGroup^> >> "test.csproj"
echo   ^<ItemGroup^> >> "test.csproj"
echo     ^<Reference Include="System" /^> >> "test.csproj"
echo     ^<Reference Include="System.Core" /^> >> "test.csproj"
echo     ^<Reference Include="System.Xml.Linq" /^> >> "test.csproj"
echo     ^<Reference Include="System.Data.DataSetExtensions" /^> >> "test.csproj"
echo     ^<Reference Include="Microsoft.CSharp" /^> >> "test.csproj"
echo     ^<Reference Include="System.Data" /^> >> "test.csproj"
echo     ^<Reference Include="System.Net.Http" /^> >> "test.csproj"
echo     ^<Reference Include="System.Xml" /^> >> "test.csproj"
echo   ^</ItemGroup^> >> "test.csproj"
echo   ^<ItemGroup^> >> "test.csproj"
goto:eof

:FinishProjFile
echo   ^</ItemGroup^> >> "test.csproj"
echo   ^<Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" /^> >> "test.csproj"
echo ^</Project^> >> "test.csproj"
goto:eof

:treeProcess
for /d %%i in (*) do (
  cd %%i
  call:CreateProjBegin
  for %%j in (*.cs) do echo     ^<Compile Include="%%j" /^> >> "test.csproj"
  call:FinishProjFile
  call:treeProcess
  cd ..
)
goto:eof

:begin
call:treeProcess