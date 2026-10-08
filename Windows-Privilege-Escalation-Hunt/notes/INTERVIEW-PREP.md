# Privilege Escalation Hunt — Learning and Interview Preparation

**Status: Preparation questions, not yet evidence of completed work.**

## Five starting concepts

1. Privilege escalation means obtaining higher privileges than previously held.
2. Local Administrators group membership changes are a valuable **indicator**, not proof of a breach.
3. Event `4732` = member added to local security group; `4733` = member removed.
4. Event `4672` = special privileges assigned to a logon; it does not itself mean someone was just promoted to administrator.
5. The hunt must distinguish actor (**Subject**) from the added account (**Member**) and affected group.

## Interview prompts

- What made the observed Administrators-group membership change worth investigating?
- What is the difference between Event 4732 and Event 4672?
- How did you confirm the group was the built-in Administrators group?
- What can cause benign administrator-group membership additions?
- What evidence links the modification to the actor account and a specific session?
- How did you test that a nonprivileged group change did not raise the same alert?
- What evidence demonstrates that you restored the original group membership?
- Which MITRE ATT&CK technique describes adding accounts to local or domain groups?

## Interview claims policy

Until the tests are run, say **"I am planning a Windows privilege escalation hunt"**, not **"I detected privilege escalation"**. Complete the interview answers only after saving authentic event evidence.

See [Project plan](../README.md), [detection plan](../detections/01-local-admin-membership.md), and [investigation template](../investigations/01-privileged-group-change.md).
