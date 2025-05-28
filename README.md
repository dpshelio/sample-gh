# sample-gh


## Process on how to run the selection

1. awaiting projects are confirmed and a yyyy-rx label gets set
2. The check duplication workflow is triggered manually, either clicking on the [action page](https://github.com/dpshelio/sample-gh/actions/workflows/duplicate.yml) or through the cli:
   ```
   gh workflow run duplicate.yml -f round=1
   ```
   
   The status of the workflow can be seen as
   
   ```
   gh run list --workflow=duplicate.yml
   ```
   If there are two issues with the same project name, they both get labelled as "duplicate" and they need to be sorted before continuing (by either closing one of them or removing the `yyyy-rx` label).
3. The boards can get then update for distributing the proposals according to the Conflict of Interest ([`CoI.yaml`](./CoI.yaml)) file. As before, either through the [Extract SDG action page](https://github.com/dpshelio/sample-gh/actions/workflows/sdg.yml) or through the CLI:
   ```
   gh workflow run sdg.yml -f round=1
   ```
4. The best proposal gets awarded the funds by the reviewers, by setting the issue with the label "awarded"
5. The rest of the issues for this round are ready to be randomised and the funds to be allocated. To do so we need to trigger the [Allocate funds workflow](https://github.com/dpshelio/sample-gh/actions/workflows/funding.yml) providing the funds available for this round, or through the CLI as:
   ```
   gh workflow run funding.yml -f round=1 -f budget=15000
   ```
   This will run the action and label as "funded" the projects that have been randomly selected.
