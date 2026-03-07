import boto3


def session():
    return boto3.session.Session()


def main():
    eks = session().client("eks")
    clusters = eks.list_clusters().get("clusters", [])
    print(f"Found {len(clusters)} EKS cluster(s):\n")

    for name in clusters:
        c = eks.describe_cluster(name=name)["cluster"]
        vpc = c.get("resourcesVpcConfig", {})
        print("---")
        print(f"Name:        {c.get('name')}")
        print(f"Status:      {c.get('status')}")
        print(f"Version:     {c.get('version')}")
        print(f"Endpoint:    {c.get('endpoint')}")
        print(f"RoleArn:     {c.get('roleArn')}")
        print(f"VPC:         {vpc.get('vpcId')}")
        print(f"Subnets:     {len(vpc.get('subnetIds', []))}")
        print(f"SecurityGps: {len(vpc.get('securityGroupIds', []))}")
    print("Done.")


if __name__ == "__main__":
    main()
