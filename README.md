# Upgrade a local Evmos node

This helper script executes all necessary commands to upgrade a local Evmos node,
that was started using the `local_node.sh` script
on the base layer of the [Evmos repository](https://github.com/evmos/evmos).

## Usage

Run a local node using the initial version, where you want to upgrade from (e.g. v12.1.4):

```bash
git checkout [INITIAL_VERSION]
./local_node.sh
```

To run the script, execute it with a target version (e.g. v13.0.0-rc2) as an input argument, while a node is running.

```bash
python3 upgrade-local-node.py [TARGET_VERSION]
```

An upgrade is scheduled for block height 25, so make sure to execute this script with sufficient time before that.
You can check the proposal status using (assuming starting a fresh node and only one proposal available):

```bash
evmosd q gov proposal 1 --node http://localhost:26657 | grep "status:"
```
