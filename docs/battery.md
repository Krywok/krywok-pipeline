# Battery (DRY)

The **Battery** module provides a DRY (Don't Repeat Yourself) pattern for sharing and reusing pipe configurations across your application. Instead of duplicating the same `type`, `conditions`, and `matches` arguments in every `Pipeline`, you define a `BatteryUnit` once and `sink()` it wherever you need it.

---

## Core Concepts

| Class         | Responsibility                                                         |
|---------------|------------------------------------------------------------------------|
| `BatteryUnit` | Stores a single pipe configuration                                     |
| `Battery`     | A centralized registry of pre-built and custom `BatteryUnit` instances |

---

## BatteryUnit

A `BatteryUnit` is a container for a reusable pipe configuration. It exposes a single method, `sink()`, which returns the stored configuration - optionally merged with field-specific overrides.

### `sink()` - Consuming a Unit

The `sink()` method is the primary way to use a `BatteryUnit`. It returns a `PipeConfig` dictionary ready to be unpacked into a `Pipeline`.

```python
from pipeline.battery import Battery

# Use a built-in unit as-is
Pipeline(
    uuid=Battery.UUID.sink()
)

# Override a specific key only for this field
Pipeline(
    email=Battery.use_email().sink(optional=True)
)
```

!!! tip "Non-Destructive Overrides"

    `sink()` merges the overrides **without** modifying the original `BatteryUnit`. The same unit can be safely reused in multiple pipelines with different overrides.

---

## Battery Registry

### `Battery.add()` - Registering Custom Units

Register your own units at application startup to make them available globally:

```python
from pipeline import Pipe
from pipeline.battery import Battery

# Register custom unit
Battery.add(
    name="Username",
    type=str,
    conditions={
        Pipe.Condition.MinLength: 3,
        Pipe.Condition.MaxLength: 20
    },
    matches={Pipe.Match.Text.Alphanumeric: None},
    transform={Pipe.Transform.Lowercase: None}
)
```

### `Battery.get()` - Retrieving Units by Name

```python
# Use it in a pipeline
Pipeline(
    username=Battery.get("Username").sink()
)
```

---

## Real-World Example

```python
from pipeline import Pipeline, Pipe
from pipeline.battery import Battery

# Register application-wide units once (e.g., in app startup)
Battery.add(
    name="ProductSKU",
    type=str,
    conditions={Pipe.Condition.ExactLength: 8},
    matches={Pipe.Match.Text.Alphanumeric: None},
    transform={Pipe.Transform.Uppercase: None}
)

# Reuse across multiple endpoints without duplication
create_order_pipeline = Pipeline(
    product_sku=Battery.get("ProductSKU").sink(),
    customer_email=Battery.use_email().sink(),
    limit=Battery.use_limit(max_number=50).sink(optional=True),
    offset=Battery.use_offset().sink(optional=True)
)

update_order_pipeline = Pipeline(
    product_sku=Battery.get("ProductSKU").sink(optional=True),
    customer_email=Battery.use_email().sink(optional=True)
)
```

---

## Technical Reference

::: pipeline.battery.unit.BatteryUnit

::: pipeline.battery.battery.Battery
