---
name: Bug report
about: Create a report to tell us about bugs you spoted
title: ''
labels: ''
assignees: ''
body:
- type: dropdown
  id: importance
  attributes:
    label: How important/disruptive is this bug?
    options:
      - Slight annoyance
      - Affects gamplay
      - Crash
  validations:
    required: true
- type: textarea
  id: desc
  attributes:
    label: Description
    description: "A clear and concise description of what the bug is."
  validations:
    required: true
- type: textarea
  id: repro
  attributes:
    label: Reproduction steps
    description: "How do you trigger this bug? Please walk us through it step by step."
    value: |
      1.
      2.
      3.
      ...
    render: bash
  validations:
    required: true
---
