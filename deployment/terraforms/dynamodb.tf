module "history_service_table" {
  source = "./../modules/dynamodb"
  hash_key = { name = "user_id", type = "S" }
  range_key = { name = "unique_id", type = "N" }
  module_name = "history_service_table"
  table_name = "justclick_history"
  verify = true
  ttl_enabled = true
  ttl_attribute_name = "ttl"
  global_secondary_indexes = [
    {
      name = "transaction_id_index"
      hash_key = {name = "transaction_id"}
    },
    {
      name = "stage_unique_id_index"
      hash_key = {name = "stage_name", type = "S"}
      range_key = {name = "unique_id", type = "N"}
    }
  ]
  stream_enabled = true
  stream_view_type = "NEW_IMAGE"
}