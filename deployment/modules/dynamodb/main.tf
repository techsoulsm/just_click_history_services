data "aws_region" "current" {}

locals {
  gsi_hash_keys = [for i in var.global_secondary_indexes: lookup(i, "hash_key") if lookup(i, "hash_key", null) != null]
  gsi_range_keys = [for i in var.global_secondary_indexes: lookup(i, "range_key") if lookup(i, "range_key", null) != null]

  gsi_hash_keys_map = zipmap([for i in local.gsi_hash_keys: lookup(i, "name")], [for i in local.gsi_hash_keys: lookup(i, "type", "S")])
  gsi_range_keys_map = zipmap([for i in local.gsi_range_keys: lookup(i, "name")], [for i in local.gsi_range_keys: lookup(i, "type", "S")])

  lsi_range_keys = [for i in var.local_secondary_indexes: lookup(i, "range_key") if lookup(i, "range_key", null) != null]
  lsi_range_keys_map = zipmap([for i in local.lsi_range_keys: lookup(i, "name")], [for i in local.lsi_range_keys: lookup(i, "type", "S")])

  hash_key_map = tomap({lookup(var.hash_key, "name") = lookup(var.hash_key, "type")})
  range_key_map = var.range_key == {} ? tomap({}) : tomap({lookup(var.range_key, "name") = lookup(var.range_key, "type", "S")})
  keys_map = merge(local.hash_key_map, local.range_key_map)

  attributes = merge(local.gsi_range_keys_map, local.gsi_hash_keys_map, local.lsi_range_keys_map, local.keys_map)
}

resource "aws_dynamodb_table" "table" {
  hash_key            = lookup(var.hash_key, "name")
  range_key           = lookup(var.range_key, "name", null)
  name                = var.table_name
  billing_mode        = var.billing_mode
  read_capacity       = var.billing_mode == "PAY_PER_REQUEST" ? null : var.read_capacity
  write_capacity      = var.billing_mode == "PAY_PER_REQUEST" ? null : var.write_capacity
  stream_enabled      = var.stream_enabled
  stream_view_type    = var.stream_view_type

  dynamic "global_secondary_index" {
    for_each          = var.global_secondary_indexes
    content {
      name            = lookup(global_secondary_index.value, "name")
      hash_key        = lookup(lookup(global_secondary_index.value, "hash_key"), "name")
      range_key       = lookup(lookup(global_secondary_index.value, "range_key", {}), "name", null)
      projection_type = lookup(global_secondary_index.value, "projection_type", "ALL")
    }
  }

  dynamic "local_secondary_index" {
    for_each          = var.local_secondary_indexes
    content {
      name            = lookup(local_secondary_index.value, "name")
      projection_type = lookup(local_secondary_index.value, "projection_type", "ALL")
      range_key       = lookup(lookup(local_secondary_index.value, "range_key", {}), "name", null)
    }
  }

  dynamic "attribute" {
    for_each          = local.attributes
    content {
      name            = attribute.key
      type            = attribute.value
    }
  }

  ttl {
    enabled        = var.ttl_enabled
    attribute_name = var.ttl_attribute_name
  }

  lifecycle {
    prevent_destroy = false
  }
}


