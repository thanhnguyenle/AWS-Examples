# AWS Route Testing Alternatives (Without VPN/BGP Setup)

## Understanding the Problem
Route propagation specifically requires:
- Virtual Private Gateway (VPN Gateway)
- BGP (Border Gateway Protocol) enabled
- On-premises router with BGP support

**Cost Reality**: Setting up a full VPN with BGP can cost $36+/month just for the VPN Gateway alone!

## Alternative 1: Basic Route Table Testing with Subnets

### What You'll Learn
- How route tables work with subnets
- Manual route creation vs automatic routes
- Route priority and evaluation

### Setup (Free tier eligible)
```bash
# 1. Create a VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# 2. Create multiple subnets
aws ec2 create-subnet --vpc-id vpc-12345678 --cidr-block 10.0.1.0/24
aws ec2 create-subnet --vpc-id vpc-12345678 --cidr-block 10.0.2.0/24

# 3. Create custom route table
aws ec2 create-route-table --vpc-id vpc-12345678

# 4. Associate subnet with route table
aws ec2 associate-route-table --subnet-id subnet-12345678 --route-table-id rtb-12345678
```

### Testing Route Behavior
```bash
# View routes (notice automatic local routes)
aws ec2 describe-route-tables --route-table-ids rtb-12345678

# Output shows automatic "local" routes for VPC CIDR:
# {
#     "DestinationCidrBlock": "10.0.0.0/16",
#     "GatewayId": "local",
#     "Origin": "static",
#     "State": "active"
# }
```

**Key Learning**: Subnets automatically get routes added to reach other subnets in the same VPC - but these are "local" routes, not "propagated" routes.

## Alternative 2: VPC Peering Route Testing

### What You'll Learn
- Cross-VPC routing without VPN
- Manual route addition
- Route table updates

### Setup
```bash
# 1. Create second VPC
aws ec2 create-vpc --cidr-block 172.16.0.0/16

# 2. Create VPC peering connection
aws ec2 create-vpc-peering-connection \
  --vpc-id vpc-12345678 \
  --peer-vpc-id vpc-87654321

# 3. Accept peering connection
aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id pcx-12345678

# 4. Add routes manually (this simulates what propagation would do automatically)
aws ec2 create-route \
  --route-table-id rtb-12345678 \
  --destination-cidr-block 172.16.0.0/16 \
  --vpc-peering-connection-id pcx-12345678
```

### Key Differences from Propagation
- **Manual**: You add routes yourself
- **Static**: Routes don't appear/disappear automatically
- **No BGP**: No dynamic routing protocol

## Alternative 3: Internet Gateway Route Testing

### What You'll Learn
- How default routes work
- Route replacement
- Target changes

### Setup
```bash
# 1. Create Internet Gateway
aws ec2 create-internet-gateway

# 2. Attach to VPC
aws ec2 attach-internet-gateway --internet-gateway-id igw-12345678 --vpc-id vpc-12345678

# 3. Add default route
aws ec2 create-route \
  --route-table-id rtb-12345678 \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id igw-12345678

# 4. View the route
aws ec2 describe-route-tables --route-table-ids rtb-12345678
```

## Alternative 4: Simulate Propagation Behavior

### Manual Simulation Script
```bash
#!/bin/bash
# simulate_propagation.sh

ROUTE_TABLE_ID="rtb-12345678"
TEST_CIDR="192.168.1.0/24"
TARGET_ID="igw-12345678"  # or any valid target

echo "=== Simulating Route Propagation ==="

# Step 1: Show routes before
echo "Routes BEFORE 'propagation':"
aws ec2 describe-route-tables --route-table-ids $ROUTE_TABLE_ID \
  --query 'RouteTables[0].Routes'

# Step 2: "Propagate" route (manually add)
echo "Adding route (simulating BGP learning)..."
aws ec2 create-route \
  --route-table-id $ROUTE_TABLE_ID \
  --destination-cidr-block $TEST_CIDR \
  --gateway-id $TARGET_ID

# Step 3: Show routes after
echo "Routes AFTER 'propagation':"
aws ec2 describe-route-tables --route-table-ids $ROUTE_TABLE_ID \
  --query 'RouteTables[0].Routes'

# Step 4: "BGP withdrawal" (remove route)
echo "Removing route (simulating BGP withdrawal)..."
aws ec2 delete-route \
  --route-table-id $ROUTE_TABLE_ID \
  --destination-cidr-block $TEST_CIDR

# Step 5: Show final state
echo "Routes AFTER 'withdrawal':"
aws ec2 describe-route-tables --route-table-ids $ROUTE_TABLE_ID \
  --query 'RouteTables[0].Routes'
```

## Alternative 5: AWS Transit Gateway (More Advanced)

### What You'll Learn
- Modern AWS routing architecture
- Route propagation concepts (similar to VPN)
- Multiple VPC connectivity

### Setup (Costs apply - about $36/month)
```bash
# 1. Create Transit Gateway
aws ec2 create-transit-gateway

# 2. Attach VPC
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id tgw-12345678 \
  --vpc-id vpc-12345678 \
  --subnet-ids subnet-12345678

# 3. Enable route propagation (similar concept to VPN)
aws ec2 enable-transit-gateway-route-table-propagation \
  --transit-gateway-attachment-id tgw-attach-12345678 \
  --transit-gateway-route-table-id tgw-rtb-12345678
```

## Key Concepts You Can Learn Without VPN

### 1. Route Types Understanding
```bash
# Local routes (automatic)
"Origin": "static", "GatewayId": "local"

# Manual routes (what you add)
"Origin": "static", "GatewayId": "igw-12345678"

# What propagated routes would look like
"Origin": "propagated", "GatewayId": "vgw-12345678"
```

### 2. Route Priority
- Most specific route wins (longest prefix match)
- Local routes have highest priority
- Propagated routes have lower priority than static

### 3. Route Table Association
```bash
# See which subnets use which route table
aws ec2 describe-route-tables \
  --query 'RouteTables[*].[RouteTableId,Associations[*].SubnetId]'
```

## Minimum VPN Setup (If You Really Want Propagation)

### Option 1: Software VPN on EC2
- Use strongSwan or OpenVPN on EC2
- Configure BGP with BIRD or FRR
- Much cheaper than managed VPN

### Option 2: AWS Client VPN
- Simpler setup
- Still allows some routing concepts
- Less expensive than Site-to-Site VPN

### Option 3: Cloud9 or EC2 with VPN Software
- Free tier eligible
- Can simulate on-premises router
- Good for learning BGP concepts

## Summary

**You CAN learn AWS routing without VPN:**
- ✅ Route table basics with subnets
- ✅ Manual route creation/deletion
- ✅ Route priorities and matching
- ✅ Cross-VPC routing with peering
- ✅ Internet gateway routing

**You CANNOT test without VPN:**
- ❌ Actual route propagation
- ❌ BGP route learning
- ❌ Automatic route appearance/disappearance
- ❌ VPN gateway specific features

The concepts are very similar - the main difference is **automatic vs manual** route management!