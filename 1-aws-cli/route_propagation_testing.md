# AWS Route Propagation Testing - Basic Example

## What We're Testing
Testing automatic route propagation from VPN Gateway to VPC Route Table using AWS CLI.

## Prerequisites
- AWS CLI configured
- VPC with VPN Gateway already set up
- On-premises router configured with BGP

## Step 1: Check Current Route Tables
```bash
# List all route tables in your VPC
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=vpc-12345678"

# Note down the route-table-id (example: rtb-12345678)
```

## Step 2: Check Current Routes (Before Propagation)
```bash
# View current routes in your route table
aws ec2 describe-route-tables --route-table-ids rtb-12345678

# Look for existing routes - should only see local routes
```

## Step 3: List Available VPN Gateways
```bash
# Find your VPN Gateway ID
aws ec2 describe-vpn-gateways

# Note down the VpnGatewayId (example: vgw-87654321)
```

## Step 4: Check VPN Gateway Route Propagation Status
```bash
# Check which route tables have propagation enabled
aws ec2 describe-route-tables \
  --filters "Name=route.propagation.gateway-id,Values=vgw-87654321"
```

## Step 5: Enable Route Propagation
```bash
# Enable route propagation from VPN Gateway to Route Table
aws ec2 enable-vgw-route-propagation \
  --route-table-id rtb-12345678 \
  --gateway-id vgw-87654321

# Expected output: No output means success
```

## Step 6: Verify Route Propagation is Enabled
```bash
# Check if propagation is now enabled
aws ec2 describe-route-tables --route-table-ids rtb-12345678 \
  --query 'RouteTables[0].PropagatingVgws'

# Expected output:
# [
#     {
#         "GatewayId": "vgw-87654321"
#     }
# ]
```

## Step 7: Check for Propagated Routes (After BGP Learning)
```bash
# View routes again to see propagated routes
aws ec2 describe-route-tables --route-table-ids rtb-12345678 \
  --query 'RouteTables[0].Routes'

# Look for routes with "Origin": "propagated"
# Example output:
# {
#     "DestinationCidrBlock": "192.168.1.0/24",
#     "GatewayId": "vgw-87654321",
#     "Origin": "propagated",
#     "State": "active"
# }
```

## Step 8: Test Route Propagation Working
```bash
# Monitor for new propagated routes (run periodically)
aws ec2 describe-route-tables --route-table-ids rtb-12345678 \
  --query 'RouteTables[0].Routes[?Origin==`propagated`]'

# This will show only propagated routes
```

## Step 9: Disable Route Propagation (For Testing)
```bash
# Disable route propagation
aws ec2 disable-vgw-route-propagation \
  --route-table-id rtb-12345678 \
  --gateway-id vgw-87654321

# Check routes are removed
aws ec2 describe-route-tables --route-table-ids rtb-12345678 \
  --query 'RouteTables[0].Routes[?Origin==`propagated`]'

# Should return empty array: []
```

## Step 10: Re-enable for Production
```bash
# Re-enable route propagation for normal operation
aws ec2 enable-vgw-route-propagation \
  --route-table-id rtb-12345678 \
  --gateway-id vgw-87654321
```

## Understanding the Output

### Route with Manual Entry:
```json
{
    "DestinationCidrBlock": "0.0.0.0/0",
    "GatewayId": "igw-12345678",
    "Origin": "static",
    "State": "active"
}
```

### Route with Propagation:
```json
{
    "DestinationCidrBlock": "192.168.1.0/24",
    "GatewayId": "vgw-87654321",
    "Origin": "propagated",
    "State": "active"
}
```

## Key Differences to Notice
- **Static routes**: Added manually by you
- **Propagated routes**: Added automatically by BGP
- **Origin field**: Shows "static" vs "propagated"

## Troubleshooting

### No Propagated Routes Appear?
```bash
# Check VPN connection status
aws ec2 describe-vpn-connections --vpn-connection-ids vpn-12345678

# Look for:
# "State": "available"
# "VgwTelemetry" -> "Status": "UP"
```

### Routes Disappear?
- Check if VPN connection is stable
- Verify on-premises router is advertising routes via BGP
- Check BGP session status

## Expected Timeline
- **Enable propagation**: Immediate
- **Routes appear**: 30 seconds to 2 minutes (after BGP learning)
- **Routes disappear**: 30 seconds to 2 minutes (after BGP withdrawal)

## Clean Up (Optional)
```bash
# Disable route propagation
aws ec2 disable-vgw-route-propagation \
  --route-table-id rtb-12345678 \
  --gateway-id vgw-87654321
```

## Summary
This test demonstrates:
1. **Manual control**: Enable/disable route propagation
2. **Automatic behavior**: Routes appear/disappear based on BGP
3. **Verification**: Distinguish between static and propagated routes
4. **Real-time**: See changes as your network topology changes