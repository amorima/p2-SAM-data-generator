import re

def validate(data, schema, context=None):
    context = context or {}

    for field, rules in schema.items():
        value = data.get(field)

        # 1. required
        if rules.get("required", False) and field not in data:
            raise ValueError(f"Missing required field: {field}")

        # 2. nullable
        if value is None:
            if not rules.get("nullable", False):
                raise ValueError(f"Field '{field}' cannot be null")
            continue

        # 3. type
        expected_type = rules.get("type")
        if expected_type and not isinstance(value, expected_type):
            raise TypeError(
                f"Field '{field}' should be {expected_type.__name__}, got {type(value).__name__}"
            )

        # 4. max_length (VARCHAR)
        max_length = rules.get("max_length")
        if max_length and isinstance(value, str) and len(value) > max_length:
            raise ValueError(f"Field '{field}' exceeds max length of {max_length}")

        # 5. regex
        regex = rules.get("regex")
        if regex and not re.match(regex, value):
            raise ValueError(f"Field '{field}' does not match regex")

        # 6. unique (com contexto)
        if rules.get("unique"):
            seen = context.setdefault(field, set())
            if value in seen:
                raise ValueError(f"Field '{field}' must be unique")
            seen.add(value)

        # 7. primary key (basic check)
        if rules.get("primary_key"):
            if value is None or value == "":
                raise ValueError(f"Primary key '{field}' inválida")

    return True