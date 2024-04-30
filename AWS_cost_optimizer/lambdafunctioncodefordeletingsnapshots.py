import boto3

def lambda_handler(event, context):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')

    # Get all snapshots
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

    # Get all volumes
    volumes = ec2.describe_volumes()['Volumes']
    attached_volume_ids = [vol['VolumeId'] for vol in volumes]

    # Delete snapshots that are not attached to any volume
    deleted_snapshots = []
    for snapshot in snapshots:
        snapshot_id = snapshot['SnapshotId']
        snapshot_volume_id = snapshot.get('VolumeId', None)
        if snapshot_volume_id not in attached_volume_ids:
            print(f"Deleting snapshot {snapshot_id} not attached to any volume.")
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            deleted_snapshots.append(snapshot_id)

    return {
        'statusCode': 200,
        'body': f"Deleted snapshots: {', '.join(deleted_snapshots)}"
    }

