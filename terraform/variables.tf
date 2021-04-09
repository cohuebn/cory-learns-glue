variable "namespace" {
  type    = string
  default = "glue-learning"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

# Note: This p.o.c. only uses one AZ. In real-life, multiple AZs should be used
variable "availability_zone" {
  type    = string
  default = "us-east-1a"
}

variable "tags" {
  type    = map(any)
  default = {}
}

variable "public_key" {
  type        = string
  description = "The public key to use to allow connection to Glue development endpoints"
  default     = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCqMnfm/kt2/Qf4tzhE1HqCHW+IVvFqjm/b86CoH6eXNq1vputYhEJy3/nwszhWkq9lsQnNq36j1fmK1V2MHxmKG9Y6UwIm6GCicdFYhFM6FxjQ8uNMdTZN6n/v6UM5+kEqQIdxZ2wYhuiIbXadrwNdLrrA51B73bzQxFh6nH2cDId0Qhoj4GfjCfi59IriuzY7i9+2H5REGMlU8cf1sp/XbXBMK0iMpq7vqu+8MmzJsBPp0wfNYn8q02lQA5WTajxqdlpm/fb756cMVJN9sgJzRG8VvcaS4KWAVWsRI3Kpt875+s4ntoQLUkZcSr4mYEL+q74Gb20GykvR2GJJoW7x huebnerc@C02Z780YLVDL"
}

variable "ip_whitelist" {
  default = [
    "198.200.139.0/24", # STL VPN
    "23.84.136.53/32",  # huebnerc
  ]
  type = list(string)
}

variable "cidr_block" {
  type        = string
  description = "The CIDR block to use for the VPC resources are created within"
  default     = "10.0.0.0/16"
}