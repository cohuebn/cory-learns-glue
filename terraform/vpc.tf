# resource "aws_vpc" "vpc" {
#   cidr_block           = var.cidr_block
#   enable_dns_hostnames = true
#   enable_dns_support   = true
#   tags                 = merge(local.tags, { Name = var.namespace })
# }

# resource "aws_internet_gateway" "vpc_public" {
#   tags   = var.tags
#   vpc_id = aws_vpc.vpc.id
# }

# resource "aws_route_table" "vpc_public" {
#   tags   = merge(var.tags, { "Name" = "${var.namespace}-public" })
#   vpc_id = aws_vpc.vpc.id

#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = aws_internet_gateway.vpc_public.id
#   }
# }

# resource "aws_vpc_endpoint" "private_s3" {
#   vpc_id       = aws_vpc.vpc.id
#   service_name = local.s3_service_name
#   tags         = local.tags
# }

# resource "aws_vpc_endpoint_route_table_association" "private_s3" {
#   route_table_id  = aws_route_table.vpc_public.id
#   vpc_endpoint_id = aws_vpc_endpoint.private_s3.id
# }

# resource "aws_subnet" "vpc_public" {
#   availability_zone       = var.availability_zone
#   cidr_block              = cidrsubnet(var.cidr_block, 8, 0)
#   map_public_ip_on_launch = true
#   tags                    = merge(var.tags, { "Name" = "${var.namespace}-public-${var.availability_zone}" })
#   vpc_id                  = aws_vpc.vpc.id
# }

# resource "aws_route_table_association" "vpc_public" {
#   subnet_id      = aws_subnet.vpc_public.id
#   route_table_id = aws_route_table.vpc_public.id
# }
