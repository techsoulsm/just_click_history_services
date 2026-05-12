variable "table_name" {

}

variable "hash_key" {

}

variable "range_key" {
  default = {}
  description = "range key"
}

variable "global_secondary_indexes" {
  default = []
  description = "list global secondary indexes eg.: [{\"index_name\" = \"name\",\"projection_type\" = \"ALL\" ,\"hash_key\" = {\"name\" = \"hash_key_1\", \"type\" = \"S\"}, \"range_key\" = {\"name\" = \"range_key_1\", \"type\" = \"S\"}}]"
}

variable "local_secondary_indexes" {
  default = []
  description = "list global secondary indexes eg.: [{\"index_name\" = \"name\", \"range_key\" = {\"name\" = \"range_key_1\", \"type\" = \"S\"}}]"
}

variable "billing_mode" {
  default = "PAY_PER_REQUEST"
  description = "dynamodb billing mode eg.: PAY_PER_REQUEST, PROVISIONED"
}

variable "read_capacity" {
  default = 5
  description = "read Capacity is used when billing mode is provisioned"
}

variable "write_capacity" {
  default = 5
  description = "write Capacity is used when billing mode is provisioned"
}

variable "stream_enabled" {
  default     = false
  description = "data to stream from dynamodb eg.: true or false"
}

variable "stream_view_type" {
  default = null
}

variable "ttl_enabled" {
  description = "Indicates whether ttl is enabled"
  type        = bool
  default     = false
}

variable "ttl_attribute_name" {
  description = "The name of the table attribute to store the TTL timestamp in"
  type        = string
  default     = ""
}

variable "region" {
  description = "region to look for table eg.: us-east-1, us-west-1 .. etc"
  default = "us-west-1"
}

variable "verify" {
  description = "check weather table exists or not if exists pass"
}

variable "state_path" {
  default = "terraform.tfstate"
  description = "path of the state file eg.:terraform.tfstate"
}

variable "module_name" {
  description = "module name given."
}