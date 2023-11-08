import * as aws from "@pulumi/aws";
import { PolicyPack, ReportViolation, validateResourceOfType } from "@pulumi/policy";

const mandatoryTags = ['Name', 'cost-center', 'owner', 'stack']

new PolicyPack("aws-typescript", {
    policies: [
        {
            name: "discouraged-ec2-public-ip-address",
            description: "Associating public IP addresses is discouraged.",
            enforcementLevel: "advisory",
            validateResource: validateResourceOfType(aws.ec2.Instance, (instance, args, reportViolation) => {
                if (instance.associatePublicIpAddress) {
                    reportViolation("Consider not setting associatePublicIpAddress to true.");
                }
            }),
        },
        {
            name: "required-mandatory-tags",
            description: `Mandatory Tags are required [ ${mandatoryTags} ]`,
            enforcementLevel: "mandatory",
            validateResource: [

                validateResourceOfType(aws.ec2.Instance, (instance, args, reportViolation) => {
                    requiredTags(instance.tags, reportViolation);
                }),
                
                validateResourceOfType(aws.ec2.Vpc, (vpc, args, reportViolation) => {
                    requiredTags(vpc.tags, reportViolation);
                }),
            ],
        },
        {
            name: "prohibited-public-internet",
            description: "Ingress rules with public internet access are prohibited.",
            enforcementLevel: "mandatory",
            validateResource: validateResourceOfType(aws.ec2.SecurityGroup, (sg, args, reportViolation) => {
                const publicInternetRules = (sg.ingress || []).find(ingressRule =>
                    (ingressRule.cidrBlocks || []).find(cidr => cidr === "0.0.0.0/0"));
                if (publicInternetRules) {
                    reportViolation("Ingress rules with public internet access are prohibited.");
                }
            }),
        }
    ],
});


function requiredTags(tags: any, reportViolation: ReportViolation) {

    mandatoryTags.forEach(tagKey => {
        if ((tags || {})[tagKey] === undefined) {
            reportViolation(`A ${tagKey} tag is missing.`);
        }
    })
}
