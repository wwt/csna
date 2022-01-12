# Placeholder directory for test.json

This is a placeholder directory for interactive debugging and program execution via the CLI

# Example actions

When running from the CLI (or using the debugger in VSCODE) you must specify a JSON file providing the action ID, config and parameter values. These examples can be saved to files in the `test_jsons` directory and referenced in the `.vscode/launch.json` file and on the command line.

`test connectivity`
-------------------

Modify `test_jsons/test.json` with this configuration, updating the values for your installation.

```json
{
    "app_config": null,
    "asset_id": "22",
    "config": {
               "smc_host": "192.0.2.1",
               "smc_username": "admin",
               "smc_password": "bigsecret",
               "smc_tenant": "example.local"
    },
    "debug_level": 3,
    "identifier": "test connectivity",
    "parameters": [
    ]
}
```
`retrieve flows`
----------------

Modify `test_jsons/flows.json` with this configuration, updating the values for your installation.

```json
{
    "app_config": null,
    "asset_id": "22",
    "config": {
               "smc_host": "192.0.2.1",
               "smc_username": "admin",
               "smc_password": "bigsecret",
               "smc_tenant": "dcloud"
    },
    "debug_level": 3,
    "identifier": "retrieve flows",
    "parameters": [
        {
            "malicious_ip": "10.201.3.20",
            "timespan": 60,
            "record_limit": 5,
            "start_time": "2022-01-05T15:30:00Z"
        }
    ]
}
```