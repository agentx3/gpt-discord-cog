{ lib
, buildPythonPackage
, fetchFromGitHub
, aiohttp
, anyio
, distro
, dirty-equals
, hatchling
, httpx
, matplotlib
, numpy
, openpyxl
, respx
, pandas
, pandas-stubs
, plotly
, pydantic
, pytest-asyncio
, pytestCheckHook
, pytest-mock
, pythonOlder
, requests
, scikit-learn
, tenacity
, tqdm
, typing-extensions
, wandb
, withOptionalDependencies ? false
}:

buildPythonPackage rec {
  pname = "openai";
  version = "1.2.4";
  format = "pyproject";

  disabled = pythonOlder "3.7.1";

  src = fetchFromGitHub {
    owner = "openai";
    repo = "openai-python";
    rev = "refs/tags/v${version}";
    hash = "sha256-AgsHvkQBLRpZeXm7diEkuhvfG+FqV7zaxoOkMoETyY4=";
  };

  propagatedBuildInputs = [
    aiohttp
    anyio
    distro
    hatchling
    httpx
    pydantic
    requests
    tqdm
  ] ++ lib.optionals (pythonOlder "3.8") [
    typing-extensions
  ] ++ lib.optionals withOptionalDependencies (builtins.attrValues {
    inherit (passthru.optional-dependencies) embeddings wandb;
  });

  passthru.optional-dependencies = {
    datalib = [
      numpy
      openpyxl
      pandas
      pandas-stubs
    ];
    embeddings = [
      matplotlib
      plotly
      scikit-learn
      tenacity
    ] ++ passthru.optional-dependencies.datalib;
    wandb = [
      wandb
    ] ++ passthru.optional-dependencies.datalib;
  };

  pythonImportsCheck = [
    "openai"
  ];

  nativeCheckInputs = [
    dirty-equals
    respx
    pytestCheckHook
    pytest-asyncio
    pytest-mock
  ];

  pytestFlagsArray = [
    "tests"
  ];

  OPENAI_API_KEY = "sk-foo";

  disabledTestPaths = [
    # Requires working instances
    "tests/api_resources"
    "tests/test_client.py"
  ];

  meta = with lib; {
    description = "Python client library for the OpenAI API";
    homepage = "https://github.com/openai/openai-python";
    changelog = "https://github.com/openai/openai-python/releases/tag/v${version}";
    license = licenses.mit;
    maintainers = with maintainers; [ agentx3 ];
  };
}
