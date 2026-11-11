# HashiCorp Terraform Enterprise Architecture Reference

Synthesized from **HashiCorp Terraform Official Documentation & Standards**.

---

## 1. Directory Structure & Module Segregation
Avoid monolithic `.tf` files. Structure repositories cleanly:

```text
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf        # Instantiates modules with dev variables
│   │   ├── terraform.tfvars
│   │   └── backend.tf     # Dev remote state configuration
│   ├── staging/
│   └── prod/
│       ├── main.tf
│       ├── terraform.tfvars
│       └── backend.tf     # Prod remote state with strict access control
└── modules/
    ├── vpc/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── eks_cluster/
    └── rds_postgres/
```

---

## 2. Remote State Management & Locking
State files contain unencrypted sensitive output (passwords, connection strings, private keys).
1. **Encryption at Rest**: Store state in remote S3/GCS buckets with AES-256 or KMS customer-managed encryption.
2. **Distributed Locking**: Configure DynamoDB table or Cloud Storage object locking to prevent concurrent `terraform apply` operations from corrupting state.
3. **State Isolation**: Never share state files between staging and production environments.

---

## 3. Defensive Variable Validation, Preconditions & Postconditions
Always define explicit types, variable validations, and lifecycle assertions:

```hcl
variable "instance_count" {
  type        = number
  description = "Number of worker nodes to deploy"
  default     = 3

  validation {
    condition     = var.instance_count >= 2 && var.instance_count <= 20
    error_message = "The instance_count must be between 2 and 20 for high availability and budget limits."
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"

  lifecycle {
    # Validated BEFORE creating/updating the resource
    precondition {
      condition     = var.environment != "prod" || var.instance_count >= 3
      error_message = "Production environments must provision at least 3 instances."
    }

    # Validated AFTER creation against live provider state
    postcondition {
      condition     = self.public_ip != ""
      error_message = "Application server must receive an allocated public IP address."
    }
  }
}
```

---

## 4. Zero-Downtime State Refactoring (`moved` Block)
When restructuring code (renaming resources, converting single items to `for_each`, or extracting resources into child modules), never run `terraform apply` blindly without a `moved` block, or Terraform will destroy and recreate the cloud resources:

```hcl
# Rename a resource in state without destroying infrastructure
moved {
  from = aws_instance.legacy_web
  to   = aws_instance.app_server
}

# Refactor a resource into a reusable child module
moved {
  from = aws_s3_bucket.media
  to   = module.storage.aws_s3_bucket.media
}
```

---

## 5. Lifecycle Rules & Drift Management
Protect critical stateful resources against accidental destruction during refactors:

```hcl
resource "aws_db_instance" "primary" {
  identifier        = "prod-db-postgres"
  engine            = "postgres"
  instance_class    = "db.r6g.xlarge"
  allocated_storage = 200

  lifecycle {
    prevent_destroy       = true
    create_before_destroy = true
    ignore_changes = [
      tags["LastModifiedBy"],
    ]
  }
}
```

- `prevent_destroy = true`: Aborts any plan or apply that would result in the deletion of the resource.
- `create_before_destroy = true`: Creates replacement infrastructure before tearing down the existing instance, minimizing service interruption.
- `ignore_changes`: Prevents Terraform from overwriting changes applied out-of-band by cloud agents or auto-scalers.
