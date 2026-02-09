# Specification Plan

This plan is only a plan. It makes no changes.

## Step 1: Decision capture
Write a short decision record that fixes the following items:
- The exact surface form of SchemaImports.
- The exact surface form of qualified names.
- Whether qualified names are always required or only on conflicts.
- Where SchemaImports is allowed: schema documents, data documents, or both.
- Resolution rules for local names versus imported names.
- Error rules for missing namespaces, duplicate namespaces, or unresolved references.

Deliverable: one page of normative decisions for review.

## Step 2: Section inventory
List every specification section that must change. The list must include:
- Surface form and markers for SchemaImports.
- Naming rules for qualified names.
- Schema resolution rules for loading imported schemas.
- Canonicalization rules for SchemaImports placement and ordering.
- Error classes and error conditions for invalid imports and namespaces.
- Formal grammar appendices.

Deliverable: a checklist of sections with exact headings.

## Step 3: Draft text
Draft the exact wording for the changes identified in Step 2.
- Keep each change in a separate block.
- Include at least one example for a schema document.
- Include at least one example for a data document.

Deliverable: draft text blocks for review.

## Step 4: Patch plan
For each draft text block, map it to the precise file locations where it will be inserted or replaced.

Deliverable: a line level change map.

## Step 5: Approval gate
Wait for approval before any edits.
