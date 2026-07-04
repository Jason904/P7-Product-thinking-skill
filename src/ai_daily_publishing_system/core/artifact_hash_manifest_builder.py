"""Pure Artifact Hash Manifest builder for caller-supplied hash fields."""

from typing import Final


ARTIFACT_HASH_MANIFEST_BUILDABLE: Final[str] = (
    "ARTIFACT_HASH_MANIFEST_BUILDABLE"
)
RUN_ID_MISSING: Final[str] = "RUN_ID_MISSING"
MANIFEST_ID_MISSING: Final[str] = "MANIFEST_ID_MISSING"
HASH_PHASE_MISSING: Final[str] = "HASH_PHASE_MISSING"
HASH_ALGORITHM_MISSING: Final[str] = "HASH_ALGORITHM_MISSING"
ARTIFACT_HASH_ENTRIES_MISSING: Final[str] = (
    "ARTIFACT_HASH_ENTRIES_MISSING"
)
ARTIFACT_HASH_ENTRY_NOT_DICT: Final[str] = (
    "ARTIFACT_HASH_ENTRY_NOT_DICT"
)
ARTIFACT_HASH_ENTRY_KEYS_INVALID: Final[str] = (
    "ARTIFACT_HASH_ENTRY_KEYS_INVALID"
)
ARTIFACT_HASH_ENTRY_FIELD_MISSING: Final[str] = (
    "ARTIFACT_HASH_ENTRY_FIELD_MISSING"
)
ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH: Final[str] = (
    "ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH"
)
DUPLICATE_ARTIFACT_HASH_ENTRY_REF: Final[str] = (
    "DUPLICATE_ARTIFACT_HASH_ENTRY_REF"
)
REQUIRED_ARTIFACT_REFS_MISSING: Final[str] = (
    "REQUIRED_ARTIFACT_REFS_MISSING"
)
MISSING_ARTIFACT_REFS_DECLARED: Final[str] = (
    "MISSING_ARTIFACT_REFS_DECLARED"
)
REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY: Final[str] = (
    "REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY"
)
HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF: Final[str] = (
    "HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF"
)
REDACTION_STATUS_MISSING: Final[str] = "REDACTION_STATUS_MISSING"
CREATED_AT_MISSING: Final[str] = "CREATED_AT_MISSING"
TIMESTAMP_POLICY_MISSING: Final[str] = "TIMESTAMP_POLICY_MISSING"
SOURCE_OF_TRUTH_MISSING: Final[str] = "SOURCE_OF_TRUTH_MISSING"
PUBLIC_URL_CREATED_TRUE: Final[str] = "PUBLIC_URL_CREATED_TRUE"
PUBLIC_URL_NON_NULL: Final[str] = "PUBLIC_URL_NON_NULL"

ARTIFACT_HASH_MANIFEST_BUILD_REASON_CODES: Final[tuple[str, ...]] = (
    RUN_ID_MISSING,
    MANIFEST_ID_MISSING,
    HASH_PHASE_MISSING,
    HASH_ALGORITHM_MISSING,
    ARTIFACT_HASH_ENTRIES_MISSING,
    ARTIFACT_HASH_ENTRY_NOT_DICT,
    ARTIFACT_HASH_ENTRY_KEYS_INVALID,
    ARTIFACT_HASH_ENTRY_FIELD_MISSING,
    ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH,
    DUPLICATE_ARTIFACT_HASH_ENTRY_REF,
    REQUIRED_ARTIFACT_REFS_MISSING,
    MISSING_ARTIFACT_REFS_DECLARED,
    REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY,
    HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF,
    REDACTION_STATUS_MISSING,
    CREATED_AT_MISSING,
    TIMESTAMP_POLICY_MISSING,
    SOURCE_OF_TRUTH_MISSING,
    PUBLIC_URL_CREATED_TRUE,
    PUBLIC_URL_NON_NULL,
    ARTIFACT_HASH_MANIFEST_BUILDABLE,
)

_SOURCE: Final[str] = (
    "artifact_hash_manifest_builder."
    "explain_artifact_hash_manifest_build"
)
_ENTRY_FIELDS: Final[tuple[str, ...]] = (
    "artifact_ref",
    "artifact_role",
    "artifact_visibility",
    "artifact_phase",
    "hash_algorithm",
    "digest",
    "digest_source",
    "redaction_status",
    "notes",
)
_ENTRY_FIELD_SET: Final[frozenset[str]] = frozenset(_ENTRY_FIELDS)
_ENTRY_STRING_FIELDS: Final[tuple[str, ...]] = (
    "artifact_ref",
    "artifact_role",
    "artifact_visibility",
    "artifact_phase",
    "hash_algorithm",
    "digest",
    "digest_source",
    "redaction_status",
)
_ENTRY_VIOLATION_REASON_PRIORITY: Final[tuple[str, ...]] = (
    ARTIFACT_HASH_ENTRY_NOT_DICT,
    ARTIFACT_HASH_ENTRY_KEYS_INVALID,
    ARTIFACT_HASH_ENTRY_FIELD_MISSING,
    ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH,
    DUPLICATE_ARTIFACT_HASH_ENTRY_REF,
    HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF,
)
_INVARIANTS: Final[tuple[str, ...]] = (
    "artifact_hash_manifest_builder_only",
    "builder_not_artifact_hash_writer",
    "builder_not_hash_calculator",
    "builder_not_hash_manager",
    "builder_not_artifact_reader",
    "builder_not_file_stat_checker",
    "builder_not_file_exists_checker",
    "builder_not_ledger_writer",
    "builder_not_gate_execution",
    "builder_not_transition_mapping",
    "builder_not_transition_execution",
    "buildable_not_artifact_hash_write",
    "buildable_not_hash_calculation",
    "buildable_not_artifact_read",
    "buildable_not_file_stat",
    "buildable_not_publish",
    "buildable_not_notification",
    "buildable_not_public_url",
    "no_runtime_context_config_or_credential_read",
    "no_adapter_preflight",
    "no_external_adapter_call",
    "no_raw_credentials",
    "no_raw_public_url",
    "no_quality_pass_no_public_url",
    "no_artifact_or_review_io",
    "no_hashlib",
    "no_hash_calculation",
    "no_ledger_write",
    "no_artifact_hash_write",
    "no_public_url_behavior",
    "no_artifact_inventory_policy_call",
    "no_gate_decision_envelope_builder_call",
    "no_run_ledger_entry_builder_call",
    "no_failure_package_builder_call",
    "no_badcase_record_builder_call",
)
_REASON_TEXT_ENTRIES: Final[tuple[tuple[str, str], ...]] = (
    (
        RUN_ID_MISSING,
        "A non-empty caller-supplied run_id is required.",
    ),
    (
        MANIFEST_ID_MISSING,
        "A non-empty caller-supplied manifest_id is required.",
    ),
    (
        HASH_PHASE_MISSING,
        "A non-empty caller-supplied hash_phase is required.",
    ),
    (
        HASH_ALGORITHM_MISSING,
        "A non-empty caller-supplied hash_algorithm is required.",
    ),
    (
        ARTIFACT_HASH_ENTRIES_MISSING,
        "At least one caller-supplied artifact hash entry is required.",
    ),
    (
        ARTIFACT_HASH_ENTRY_NOT_DICT,
        "Every caller-supplied artifact hash entry must be a plain dict.",
    ),
    (
        ARTIFACT_HASH_ENTRY_KEYS_INVALID,
        "Every artifact hash entry must contain exactly the approved "
        "entry keys.",
    ),
    (
        ARTIFACT_HASH_ENTRY_FIELD_MISSING,
        "Every artifact hash entry requires non-empty caller-supplied "
        "string fields and tuple notes.",
    ),
    (
        ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH,
        "Every entry hash_algorithm must match the manifest hash_algorithm.",
    ),
    (
        DUPLICATE_ARTIFACT_HASH_ENTRY_REF,
        "Each non-empty artifact_ref may appear in only one hash entry.",
    ),
    (
        REQUIRED_ARTIFACT_REFS_MISSING,
        "At least one caller-supplied required_artifact_ref is required.",
    ),
    (
        MISSING_ARTIFACT_REFS_DECLARED,
        "A buildable manifest cannot declare missing artifact refs.",
    ),
    (
        REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY,
        "Every required_artifact_ref must have a caller-supplied hash entry.",
    ),
    (
        HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF,
        "Every hash entry artifact_ref must be declared as required or "
        "optional.",
    ),
    (
        REDACTION_STATUS_MISSING,
        "A non-empty caller-supplied redaction_status is required.",
    ),
    (
        CREATED_AT_MISSING,
        "A non-empty caller-supplied created_at value is required.",
    ),
    (
        TIMESTAMP_POLICY_MISSING,
        "A non-empty caller-supplied timestamp_policy is required.",
    ),
    (
        SOURCE_OF_TRUTH_MISSING,
        "At least one caller-supplied source_of_truth reference is required.",
    ),
    (
        PUBLIC_URL_CREATED_TRUE,
        "MVP artifact hash manifests require public_url_created to remain "
        "false.",
    ),
    (
        PUBLIC_URL_NON_NULL,
        "MVP artifact hash manifests require the caller-supplied public URL "
        "null marker to remain true.",
    ),
    (
        ARTIFACT_HASH_MANIFEST_BUILDABLE,
        "The caller-supplied fields can build the Artifact Hash Manifest "
        "shape. This does not write artifact-hash.yaml, calculate a hash, "
        "read artifacts, check file existence or stat metadata, write a "
        "ledger, execute a gate, map or execute a transition, publish, "
        "send notification, create or return a public URL, read runtime "
        "context, configuration, credentials, adapter outputs, artifacts, "
        "reviews, hashes or ledgers, call existing policy or builder "
        "modules, or call an external service.",
    ),
)
_VIOLATION_FIELD_ENTRIES: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    (RUN_ID_MISSING, ("run_id",)),
    (MANIFEST_ID_MISSING, ("manifest_id",)),
    (HASH_PHASE_MISSING, ("hash_phase",)),
    (HASH_ALGORITHM_MISSING, ("hash_algorithm",)),
    (ARTIFACT_HASH_ENTRIES_MISSING, ("artifact_hash_entries",)),
    (REQUIRED_ARTIFACT_REFS_MISSING, ("required_artifact_refs",)),
    (MISSING_ARTIFACT_REFS_DECLARED, ("missing_artifact_refs",)),
    (
        REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY,
        ("required_artifact_refs",),
    ),
    (REDACTION_STATUS_MISSING, ("redaction_status",)),
    (CREATED_AT_MISSING, ("created_at",)),
    (TIMESTAMP_POLICY_MISSING, ("timestamp_policy",)),
    (SOURCE_OF_TRUTH_MISSING, ("source_of_truth",)),
    (PUBLIC_URL_CREATED_TRUE, ("public_url_created",)),
    (PUBLIC_URL_NON_NULL, ("public_url",)),
)


def _reason_text(reason_code: str) -> str:
    for code, text in _REASON_TEXT_ENTRIES:
        if code == reason_code:
            return text
    return "Unknown Artifact Hash Manifest build result."


def _ordered_unique(values: tuple[str, ...]) -> tuple[str, ...]:
    ordered_values = ()
    for value in values:
        if value not in ordered_values:
            ordered_values = ordered_values + (value,)
    return ordered_values


def _entry_artifact_ref(entry) -> str:
    if isinstance(entry, dict) is False:
        return ""
    artifact_ref = entry.get("artifact_ref")
    if isinstance(artifact_ref, str):
        return artifact_ref
    return ""


def _entry_missing_fields(entry) -> tuple[str, ...]:
    fields = ()
    for field_name in _ENTRY_STRING_FIELDS:
        value = entry.get(field_name)
        if isinstance(value, str) is False or value.strip() == "":
            fields = fields + (f"artifact_hash_entries[].{field_name}",)
    if isinstance(entry.get("notes"), tuple) is False:
        fields = fields + ("artifact_hash_entries[].notes",)
    return fields


def _entry_violation(
    *,
    entry_index: int,
    artifact_ref: str,
    reason_code: str,
    fields: tuple[str, ...],
) -> dict[str, object]:
    return {
        "entry_index": entry_index,
        "artifact_ref": artifact_ref,
        "reason_code": reason_code,
        "fields": fields,
    }


def _entry_reason_priority(reason_code: str) -> int:
    for index, prioritized_reason_code in enumerate(
        _ENTRY_VIOLATION_REASON_PRIORITY
    ):
        if reason_code == prioritized_reason_code:
            return index
    return len(_ENTRY_VIOLATION_REASON_PRIORITY)


def _entry_violation_sort_key(
    violation: dict[str, object],
) -> tuple[int, int]:
    return (
        _entry_reason_priority(str(violation["reason_code"])),
        int(violation["entry_index"]),
    )


def _sorted_entry_violations(
    violations: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(sorted(violations, key=_entry_violation_sort_key))


def _entry_violations(
    artifact_hash_entries: tuple[dict[str, object], ...],
    hash_algorithm: str,
    required_artifact_refs: tuple[str, ...],
    optional_artifact_refs: tuple[str, ...],
) -> tuple[dict[str, object], ...]:
    violations = ()
    seen_artifact_refs = ()
    declared_artifact_refs = required_artifact_refs + optional_artifact_refs
    manifest_hash_algorithm_present = hash_algorithm.strip() != ""

    for entry_index, entry in enumerate(artifact_hash_entries):
        artifact_ref = _entry_artifact_ref(entry)
        if isinstance(entry, dict) is False:
            violations = violations + (
                _entry_violation(
                    entry_index=entry_index,
                    artifact_ref="",
                    reason_code=ARTIFACT_HASH_ENTRY_NOT_DICT,
                    fields=("artifact_hash_entries[]",),
                ),
            )
            continue

        entry_keys_valid = frozenset(entry) == _ENTRY_FIELD_SET
        if entry_keys_valid is False:
            violations = violations + (
                _entry_violation(
                    entry_index=entry_index,
                    artifact_ref=artifact_ref,
                    reason_code=ARTIFACT_HASH_ENTRY_KEYS_INVALID,
                    fields=("artifact_hash_entries[].keys",),
                ),
            )

        missing_fields = _entry_missing_fields(entry)
        if missing_fields != ():
            violations = violations + (
                _entry_violation(
                    entry_index=entry_index,
                    artifact_ref=artifact_ref,
                    reason_code=ARTIFACT_HASH_ENTRY_FIELD_MISSING,
                    fields=missing_fields,
                ),
            )

        entry_hash_algorithm = entry.get("hash_algorithm")
        if (
            manifest_hash_algorithm_present
            and entry_keys_valid
            and isinstance(entry_hash_algorithm, str)
            and entry_hash_algorithm.strip() != ""
            and entry_hash_algorithm != hash_algorithm
        ):
            violations = violations + (
                _entry_violation(
                    entry_index=entry_index,
                    artifact_ref=artifact_ref,
                    reason_code=ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH,
                    fields=("artifact_hash_entries[].hash_algorithm",),
                ),
            )

        if artifact_ref.strip() != "":
            if artifact_ref in seen_artifact_refs:
                violations = violations + (
                    _entry_violation(
                        entry_index=entry_index,
                        artifact_ref=artifact_ref,
                        reason_code=DUPLICATE_ARTIFACT_HASH_ENTRY_REF,
                        fields=("artifact_hash_entries[].artifact_ref",),
                    ),
                )
            else:
                seen_artifact_refs = seen_artifact_refs + (artifact_ref,)

            if artifact_ref not in declared_artifact_refs:
                violations = violations + (
                    _entry_violation(
                        entry_index=entry_index,
                        artifact_ref=artifact_ref,
                        reason_code=HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF,
                        fields=("artifact_hash_entries[].artifact_ref",),
                    ),
                )

    return _sorted_entry_violations(violations)


def _entry_refs(
    artifact_hash_entries: tuple[dict[str, object], ...],
) -> tuple[str, ...]:
    refs = ()
    for entry in artifact_hash_entries:
        artifact_ref = _entry_artifact_ref(entry)
        if artifact_ref.strip() != "":
            refs = refs + (artifact_ref,)
    return refs


def _entry_reason_present(
    entry_violations: tuple[dict[str, object], ...],
    reason_code: str,
) -> bool:
    for violation in entry_violations:
        if violation["reason_code"] == reason_code:
            return True
    return False


def _required_ref_without_entry(
    required_artifact_refs: tuple[str, ...],
    artifact_hash_entries: tuple[dict[str, object], ...],
) -> bool:
    entry_refs = _entry_refs(artifact_hash_entries)
    for required_artifact_ref in required_artifact_refs:
        if required_artifact_ref not in entry_refs:
            return True
    return False


def _missing_or_invalid_fields(
    manifest_violations: tuple[str, ...],
    entry_violations: tuple[dict[str, object], ...],
) -> tuple[str, ...]:
    field_names = ()
    for violation in manifest_violations:
        for reason_code, invalid_fields in _VIOLATION_FIELD_ENTRIES:
            if violation == reason_code:
                field_names = field_names + invalid_fields
        for entry_violation in entry_violations:
            if entry_violation["reason_code"] == violation:
                field_names = field_names + entry_violation["fields"]
    return _ordered_unique(field_names)


def _sanitized_entry(entry) -> dict[str, object]:
    if isinstance(entry, dict) is False:
        return {
            "artifact_ref": "",
            "artifact_role": "",
            "artifact_visibility": "",
            "artifact_phase": "",
            "hash_algorithm": "",
            "digest": "",
            "digest_source": "",
            "redaction_status": "",
            "notes": (),
        }

    return {
        "artifact_ref": (
            entry["artifact_ref"]
            if isinstance(entry.get("artifact_ref"), str)
            else ""
        ),
        "artifact_role": (
            entry["artifact_role"]
            if isinstance(entry.get("artifact_role"), str)
            else ""
        ),
        "artifact_visibility": (
            entry["artifact_visibility"]
            if isinstance(entry.get("artifact_visibility"), str)
            else ""
        ),
        "artifact_phase": (
            entry["artifact_phase"]
            if isinstance(entry.get("artifact_phase"), str)
            else ""
        ),
        "hash_algorithm": (
            entry["hash_algorithm"]
            if isinstance(entry.get("hash_algorithm"), str)
            else ""
        ),
        "digest": (
            entry["digest"] if isinstance(entry.get("digest"), str) else ""
        ),
        "digest_source": (
            entry["digest_source"]
            if isinstance(entry.get("digest_source"), str)
            else ""
        ),
        "redaction_status": (
            entry["redaction_status"]
            if isinstance(entry.get("redaction_status"), str)
            else ""
        ),
        "notes": entry["notes"] if isinstance(entry.get("notes"), tuple) else (),
    }


def _manifest(
    *,
    run_id: str,
    manifest_id: str,
    hash_phase: str,
    hash_algorithm: str,
    artifact_hash_entries: tuple[dict[str, object], ...],
    required_artifact_refs: tuple[str, ...],
    optional_artifact_refs: tuple[str, ...],
    missing_artifact_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "manifest_id": manifest_id,
        "hash_phase": hash_phase,
        "hash_algorithm": hash_algorithm,
        "artifact_hash_entries": tuple(
            _sanitized_entry(entry) for entry in artifact_hash_entries
        ),
        "required_artifact_refs": required_artifact_refs,
        "optional_artifact_refs": optional_artifact_refs,
        "missing_artifact_refs": missing_artifact_refs,
        "redaction_status": redaction_status,
        "public_url_created": public_url_created,
        "public_url": None,
        "created_at": created_at,
        "timestamp_policy": timestamp_policy,
        "source_of_truth": source_of_truth,
        "notes": notes,
    }


def _result(
    *,
    buildable: bool,
    reason_code: str,
    manifest,
    manifest_violations: tuple[str, ...],
    missing_or_invalid_fields: tuple[str, ...],
    entry_violations: tuple[dict[str, object], ...],
) -> dict[str, object]:
    return {
        "buildable": buildable,
        "reason_code": reason_code,
        "reason": _reason_text(reason_code),
        "source": _SOURCE,
        "manifest": manifest,
        "manifest_violations": manifest_violations,
        "missing_or_invalid_fields": missing_or_invalid_fields,
        "entry_violations": entry_violations,
        "invariant_refs": _INVARIANTS,
    }


def explain_artifact_hash_manifest_build(
    *,
    run_id: str,
    manifest_id: str,
    hash_phase: str,
    hash_algorithm: str,
    artifact_hash_entries: tuple[dict[str, object], ...],
    required_artifact_refs: tuple[str, ...],
    optional_artifact_refs: tuple[str, ...],
    missing_artifact_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> dict[str, object]:
    """Explain whether caller-supplied fields can build the manifest."""
    entry_violations = _entry_violations(
        artifact_hash_entries=artifact_hash_entries,
        hash_algorithm=hash_algorithm,
        required_artifact_refs=required_artifact_refs,
        optional_artifact_refs=optional_artifact_refs,
    )
    prioritized_violations = (
        (run_id.strip() == "", RUN_ID_MISSING),
        (manifest_id.strip() == "", MANIFEST_ID_MISSING),
        (hash_phase.strip() == "", HASH_PHASE_MISSING),
        (hash_algorithm.strip() == "", HASH_ALGORITHM_MISSING),
        (artifact_hash_entries == (), ARTIFACT_HASH_ENTRIES_MISSING),
        (
            _entry_reason_present(
                entry_violations,
                ARTIFACT_HASH_ENTRY_NOT_DICT,
            ),
            ARTIFACT_HASH_ENTRY_NOT_DICT,
        ),
        (
            _entry_reason_present(
                entry_violations,
                ARTIFACT_HASH_ENTRY_KEYS_INVALID,
            ),
            ARTIFACT_HASH_ENTRY_KEYS_INVALID,
        ),
        (
            _entry_reason_present(
                entry_violations,
                ARTIFACT_HASH_ENTRY_FIELD_MISSING,
            ),
            ARTIFACT_HASH_ENTRY_FIELD_MISSING,
        ),
        (
            _entry_reason_present(
                entry_violations,
                ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH,
            ),
            ARTIFACT_HASH_ENTRY_ALGORITHM_MISMATCH,
        ),
        (
            _entry_reason_present(
                entry_violations,
                DUPLICATE_ARTIFACT_HASH_ENTRY_REF,
            ),
            DUPLICATE_ARTIFACT_HASH_ENTRY_REF,
        ),
        (required_artifact_refs == (), REQUIRED_ARTIFACT_REFS_MISSING),
        (missing_artifact_refs != (), MISSING_ARTIFACT_REFS_DECLARED),
        (
            required_artifact_refs != ()
            and artifact_hash_entries != ()
            and _entry_reason_present(
                entry_violations,
                ARTIFACT_HASH_ENTRY_NOT_DICT,
            )
            is False
            and _required_ref_without_entry(
                required_artifact_refs,
                artifact_hash_entries,
            ),
            REQUIRED_ARTIFACT_REF_WITHOUT_HASH_ENTRY,
        ),
        (
            required_artifact_refs != ()
            and _entry_reason_present(
                entry_violations,
                HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF,
            ),
            HASH_ENTRY_FOR_UNDECLARED_ARTIFACT_REF,
        ),
        (redaction_status.strip() == "", REDACTION_STATUS_MISSING),
        (created_at.strip() == "", CREATED_AT_MISSING),
        (timestamp_policy.strip() == "", TIMESTAMP_POLICY_MISSING),
        (source_of_truth == (), SOURCE_OF_TRUTH_MISSING),
        (public_url_created is True, PUBLIC_URL_CREATED_TRUE),
        (public_url_is_null is False, PUBLIC_URL_NON_NULL),
    )
    manifest_violations = tuple(
        reason_code
        for condition, reason_code in prioritized_violations
        if condition
    )
    buildable = manifest_violations == ()
    reason_code = (
        ARTIFACT_HASH_MANIFEST_BUILDABLE
        if buildable
        else manifest_violations[0]
    )

    return _result(
        buildable=buildable,
        reason_code=reason_code,
        manifest=_manifest(
            run_id=run_id,
            manifest_id=manifest_id,
            hash_phase=hash_phase,
            hash_algorithm=hash_algorithm,
            artifact_hash_entries=artifact_hash_entries,
            required_artifact_refs=required_artifact_refs,
            optional_artifact_refs=optional_artifact_refs,
            missing_artifact_refs=missing_artifact_refs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        ),
        manifest_violations=manifest_violations,
        missing_or_invalid_fields=_missing_or_invalid_fields(
            manifest_violations,
            entry_violations,
        ),
        entry_violations=entry_violations,
    )


def is_artifact_hash_manifest_buildable(
    *,
    run_id: str,
    manifest_id: str,
    hash_phase: str,
    hash_algorithm: str,
    artifact_hash_entries: tuple[dict[str, object], ...],
    required_artifact_refs: tuple[str, ...],
    optional_artifact_refs: tuple[str, ...],
    missing_artifact_refs: tuple[str, ...],
    redaction_status: str,
    public_url_created: bool,
    public_url_is_null: bool,
    created_at: str,
    timestamp_policy: str,
    source_of_truth: tuple[str, ...],
    notes: tuple[str, ...],
) -> bool:
    """Return only the boolean result from the build explanation."""
    return bool(
        explain_artifact_hash_manifest_build(
            run_id=run_id,
            manifest_id=manifest_id,
            hash_phase=hash_phase,
            hash_algorithm=hash_algorithm,
            artifact_hash_entries=artifact_hash_entries,
            required_artifact_refs=required_artifact_refs,
            optional_artifact_refs=optional_artifact_refs,
            missing_artifact_refs=missing_artifact_refs,
            redaction_status=redaction_status,
            public_url_created=public_url_created,
            public_url_is_null=public_url_is_null,
            created_at=created_at,
            timestamp_policy=timestamp_policy,
            source_of_truth=source_of_truth,
            notes=notes,
        )["buildable"]
    )
