import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def draw_header(c, width, height, title, subtitle):
    # Top banner
    c.setFillColor(colors.HexColor("#1A237E")) # Deep indigo
    c.rect(0, height - 55, width, 55, fill=1, stroke=0)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 30, title)
    
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#E0E7FF"))
    c.drawString(30, height - 46, subtitle)

    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 30, height - 30, "AWS Production Infrastructure")
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 30, height - 44, "DevOps Architecture Blueprint | Terraform + ECS Fargate")

def draw_footer(c, width, height, page_num, total_pages):
    c.setStrokeColor(colors.HexColor("#BDBDBD"))
    c.setLineWidth(0.5)
    c.line(30, 25, width - 30, 25)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#616161"))
    c.drawString(30, 14, "NestJS Notes/Todo Application  *  Automated Terraform IaC  *  GitLab CI / GitHub Actions")
    c.drawRightString(width - 30, 14, f"Page {page_num} of {total_pages}")

def draw_diagram_page(filename):
    width, height = landscape(A4) # 841.89 x 595.28 pt
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    
    # 1. Header
    draw_header(c, width, height, 
                "AWS Production Architecture: NestJS Todo App", 
                "High-Availability Serverless Architecture with ECS Fargate, Multi-AZ VPC, ALB & CI/CD")
    
    # 2. Main Background / Outer Container: AWS Cloud (Region: eu-central-1)
    # Bounds: x=140, y=45, w=540, h=485
    c.setStrokeColor(colors.HexColor("#1E88E5"))
    c.setLineWidth(1.5)
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.roundRect(140, 45, 540, 485, 8, fill=1, stroke=1)
    
    # AWS Cloud Title
    c.setFillColor(colors.HexColor("#0D47A1"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(155, 513, "AWS Cloud Region: eu-central-1 (Frankfurt)")
    
    # 3. VPC Container: 10.0.0.0/16
    # Bounds: x=155, y=55, w=510, h=445
    c.setStrokeColor(colors.HexColor("#0288D1"))
    c.setLineWidth(1.2)
    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.roundRect(155, 55, 510, 445, 6, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor("#01579B"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(170, 486, "VPC: 10.0.0.0/16 (Custom Isolated Virtual Private Cloud)")
    
    # Internet Gateway (IGW) box
    c.setFillColor(colors.HexColor("#7B1FA2"))
    c.roundRect(170, 445, 150, 26, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(245, 454, "Internet Gateway (IGW)")

    # 4. Public Subnets Tier (Green)
    # Bounds: x=170, y=70, w=235, h=365
    c.setStrokeColor(colors.HexColor("#2E7D32"))
    c.setLineWidth(1)
    c.setFillColor(colors.HexColor("#F1F8E9"))
    c.roundRect(170, 70, 235, 365, 5, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor("#1B5E20"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(180, 420, "Public Subnets Tier (DMZ)")
    
    # Public Subnet AZ-a
    c.setStrokeColor(colors.HexColor("#81C784"))
    c.setFillColor(colors.HexColor("#E8F5E9"))
    c.roundRect(180, 280, 215, 130, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#2E7D32"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(190, 396, "Public Subnet 1: 10.0.1.0/24 (AZ-a)")
    
    # NAT Gateway box inside AZ-a
    c.setFillColor(colors.HexColor("#E65100"))
    c.roundRect(190, 345, 195, 36, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(200, 365, "NAT Gateway (Elastic IP)")
    c.setFont("Helvetica", 7.5)
    c.drawString(200, 352, "Outbound Egress IP: 52.57.225.16")
    
    # ALB block spanning across Public Subnets
    c.setFillColor(colors.HexColor("#2E7D32"))
    c.roundRect(190, 210, 195, 60, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(200, 252, "Application Load Balancer (ALB)")
    c.setFont("Helvetica", 7.5)
    c.drawString(200, 240, "* Listener HTTP:80 -> HTTPS:443 (Redirect)")
    c.drawString(200, 228, "* Listener HTTPS:443 (ACM SSL Certificate)")
    c.drawString(200, 216, "* Target Group Health Check: /api/v1 (200 OK)")

    # Public Subnet AZ-b
    c.setStrokeColor(colors.HexColor("#81C784"))
    c.setFillColor(colors.HexColor("#E8F5E9"))
    c.roundRect(180, 80, 215, 115, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#2E7D32"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(190, 180, "Public Subnet 2: 10.0.2.0/24 (AZ-b)")
    
    c.setFillColor(colors.HexColor("#43A047"))
    c.roundRect(190, 110, 195, 55, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(200, 148, "ALB Secondary Availability Zone")
    c.setFont("Helvetica", 7.5)
    c.drawString(200, 134, "* Redundant Multi-AZ Load Balancing")
    c.drawString(200, 122, "* Automated Failover Support")

    # 5. Private Subnets Tier (Blue/Orange - ECS Fargate)
    # Bounds: x=420, y=70, w=235, h=365
    c.setStrokeColor(colors.HexColor("#1565C0"))
    c.setLineWidth(1)
    c.setFillColor(colors.HexColor("#E3F2FD"))
    c.roundRect(420, 70, 235, 365, 5, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor("#0D47A1"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(430, 420, "Private Subnets Tier (Isolated - No Public IP)")
    
    # ECS Cluster outline
    c.setStrokeColor(colors.HexColor("#FF8F00"))
    c.setLineWidth(1)
    c.setFillColor(colors.HexColor("#FFF8E1"))
    c.roundRect(428, 80, 219, 325, 5, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#E65100"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(438, 390, "AWS ECS Cluster (Fargate Serverless)")

    # Private Subnet AZ-a Task
    c.setFillColor(colors.HexColor("#FB8C00"))
    c.roundRect(438, 280, 199, 95, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(448, 360, "ECS Task 1 (AZ-a: 10.0.10.0/24)")
    c.setFont("Helvetica", 7.5)
    c.drawString(448, 346, "* NestJS Docker Container")
    c.drawString(448, 334, "* Port: 3000 (Strictly Internal)")
    c.drawString(448, 322, "* SG: Ingress ONLY from ALB SG!")
    c.drawString(448, 310, "* CPU: 256 (.25 vCPU) | RAM: 512 MB")
    c.drawString(448, 296, "* Egress -> NAT Gateway (Outbound)")

    # Private Subnet AZ-b Task
    c.setFillColor(colors.HexColor("#FB8C00"))
    c.roundRect(438, 170, 199, 95, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(448, 250, "ECS Task 2 (AZ-b: 10.0.11.0/24)")
    c.setFont("Helvetica", 7.5)
    c.drawString(448, 236, "* NestJS Docker Container")
    c.drawString(448, 224, "* Port: 3000 (Strictly Internal)")
    c.drawString(448, 212, "* SG: Ingress ONLY from ALB SG!")
    c.drawString(448, 200, "* CPU: 256 (.25 vCPU) | RAM: 512 MB")
    c.drawString(448, 186, "* High Availability Replica")

    # IAM Roles Card inside ECS
    c.setFillColor(colors.HexColor("#455A64"))
    c.roundRect(438, 90, 199, 65, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(448, 142, "IAM Security Roles")
    c.setFont("Helvetica", 7)
    c.drawString(448, 130, "* ecsTaskExecutionRole:")
    c.drawString(456, 120, "ECR pull image & CloudWatch logging")
    c.drawString(448, 108, "* ecsTaskRole: App runtime permissions")

    # 6. Left Elements: User, Route 53, ACM
    # Users
    c.setFillColor(colors.HexColor("#263238"))
    c.roundRect(15, 230, 105, 55, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(67, 266, "End Users / Clients")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(67, 252, "Web Browser")
    c.drawCentredString(67, 240, "HTTPS : 443")

    # Route 53 DNS
    c.setFillColor(colors.HexColor("#6A1B9A"))
    c.roundRect(15, 320, 105, 55, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(67, 356, "Amazon Route 53")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(67, 342, "DNS Routing")
    c.drawCentredString(67, 330, "api.example.com")

    # ACM
    c.setFillColor(colors.HexColor("#C2185B"))
    c.roundRect(15, 410, 105, 55, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(67, 446, "AWS Certificate Mgr")
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(67, 432, "ACM SSL / TLS")
    c.drawCentredString(67, 420, "Auto-renewing Cert")

    # 7. Right Elements: CloudWatch, ECR, MongoDB Atlas
    # CloudWatch Logs
    c.setFillColor(colors.HexColor("#C2185B"))
    c.roundRect(700, 410, 125, 60, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(710, 456, "Amazon CloudWatch")
    c.setFont("Helvetica", 7.5)
    c.drawString(710, 442, "Logs Group:")
    c.drawString(710, 430, "/ecs/nestjs-todo")
    c.drawString(710, 418, "Retention: 14 days")

    # Amazon ECR
    c.setFillColor(colors.HexColor("#E65100"))
    c.roundRect(700, 310, 125, 65, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(710, 360, "Amazon ECR (Private)")
    c.setFont("Helvetica", 7.5)
    c.drawString(710, 346, "Docker Container Repo")
    c.drawString(710, 334, "nestjs-todo-production")
    c.drawString(710, 322, "Lifecycle: Last 10 imgs")

    # MongoDB Atlas Cloud (External)
    c.setFillColor(colors.HexColor("#13AA52")) # Official Mongo Green
    c.roundRect(700, 170, 125, 95, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(710, 250, "MongoDB Atlas Cloud")
    c.setFont("Helvetica", 7.5)
    c.drawString(710, 236, "* Managed Cluster M0")
    c.drawString(710, 224, "* Collection: notes_todo")
    c.drawString(710, 210, "* Network Security:")
    c.drawString(714, 198, "Whitelisted NAT IP")
    c.drawString(714, 184, "52.57.225.16 / 0.0.0.0/0")

    # 8. Bottom CI/CD Workflow
    # CI/CD Container
    c.setFillColor(colors.HexColor("#E64A19"))
    c.roundRect(700, 50, 125, 95, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(710, 130, "CI/CD Pipelines")
    c.setFont("Helvetica", 7.5)
    c.drawString(710, 116, "GitLab CI / GitHub")
    c.drawString(710, 102, "1. npm run test")
    c.drawString(710, 90, "2. docker build & push")
    c.drawString(710, 78, "3. aws ecs update-srv")
    c.drawString(710, 64, "Zero Downtime Deploy")

    # 9. Draw Flow Connecting Lines & Arrows
    c.setStrokeColor(colors.HexColor("#37474F"))
    c.setLineWidth(1.5)

    def draw_triangle(p_list):
        p = c.beginPath()
        p.moveTo(p_list[0], p_list[1])
        p.lineTo(p_list[2], p_list[3])
        p.lineTo(p_list[4], p_list[5])
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    # User -> ALB
    c.line(120, 255, 190, 255)
    draw_triangle([185, 258, 190, 255, 185, 252])

    # ALB -> ECS Tasks
    c.setStrokeColor(colors.HexColor("#2E7D32"))
    c.line(385, 250, 410, 250)
    c.line(410, 250, 410, 325)
    c.line(410, 325, 438, 325) # To Task 1
    draw_triangle([433, 328, 438, 325, 433, 322])

    c.line(410, 250, 410, 215)
    c.line(410, 215, 438, 215) # To Task 2
    draw_triangle([433, 218, 438, 215, 433, 212])

    # ECS Tasks -> NAT Gateway (Outbound)
    c.setStrokeColor(colors.HexColor("#E65100"))
    c.setDash(3, 3)
    c.line(537, 375, 537, 435)
    c.line(537, 435, 287, 435)
    c.line(287, 435, 287, 381) # into NAT GW
    draw_triangle([284, 386, 287, 381, 290, 386])

    # NAT Gateway -> MongoDB Atlas (Egress)
    c.setStrokeColor(colors.HexColor("#13AA52"))
    c.line(287, 381, 287, 455)
    c.line(287, 455, 680, 455)
    c.line(680, 455, 680, 220)
    c.line(680, 220, 700, 220)
    draw_triangle([695, 223, 700, 220, 695, 217])

    # ECS Tasks -> CloudWatch (Logs)
    c.setStrokeColor(colors.HexColor("#C2185B"))
    c.line(637, 335, 685, 335)
    c.line(685, 335, 685, 440)
    c.line(685, 440, 700, 440)
    draw_triangle([695, 443, 700, 440, 695, 437])

    # CI/CD -> ECR -> ECS
    c.setStrokeColor(colors.HexColor("#E64A19"))
    c.line(762, 145, 762, 310)
    draw_triangle([759, 305, 762, 310, 765, 305])

    c.setDash() # reset dash
    draw_footer(c, width, height, 1, 2)
    c.showPage()
    
    # ----------------------------------------------------
    # PAGE 2: Technical Specification & Infrastructure Matrix
    # ----------------------------------------------------
    draw_header(c, width, height,
                "AWS Infrastructure Specification & Technical Matrix",
                "Detailed Inventory of Provisioned Cloud Resources, Security Policies & CI/CD Stages")
    
    # We will build a structured table on Page 2
    # Table bounds
    data = [
        ["Resource / Component", "AWS Service", "Network Zone / Placement", "Security & Ports", "Role / Specification"],
        ["Virtual Private Cloud", "AWS VPC", "eu-central-1 (10.0.0.0/16)", "DNS Hostnames: Enabled", "Isolated virtual network environment"],
        ["Public Subnet 1 & 2", "VPC Subnet", "Multi-AZ: eu-central-1a & 1b", "CIDR: 10.0.1.0/24, 10.0.2.0/24", "Hosts Internet-facing ALB and NAT Gateway"],
        ["Private Subnet 1 & 2", "VPC Subnet", "Multi-AZ: eu-central-1a & 1b", "CIDR: 10.0.10.0/24, 10.0.11.0/24", "Hosts ECS Tasks (Strictly no Public IP)"],
        ["Internet Gateway (IGW)", "VPC IGW", "VPC Edge (Attached)", "Ingress / Egress 0.0.0.0/0", "Connects VPC Public subnets to Internet"],
        ["NAT Gateway", "AWS NAT GW", "Public Subnet 1 (AZ-a)", "Elastic IP: 52.57.225.16", "Provides outbound Internet access for ECS tasks"],
        ["Application Load Balancer", "AWS ALB", "Public Subnets (Multi-AZ)", "SG Ingress: TCP 80 & 443", "Routes traffic, terminates SSL, Health Checks"],
        ["ALB Target Group", "AWS Target Group", "VPC Internal (IP Target Type)", "Health Path: /api/v1 (200 OK)", "Deregistration delay: 30s, health check: 30s"],
        ["ECS Cluster", "AWS ECS Fargate", "VPC Private Subnets", "Fargate Serverless", "Auto-healing, container management, no EC2 instances"],
        ["ECS Tasks (2 Replicas)", "ECS Task Definition", "Private Subnets (Multi-AZ)", "Port 3000 Ingress ONLY from ALB", "NestJS App, CPU: 256, RAM: 512MB, env: DATABASE_URI"],
        ["Container Registry", "Amazon ECR", "AWS Managed (Private)", "Encrypted, Scan on push", "Stores Docker images with short SHA and latest tags"],
        ["Log Monitoring", "CloudWatch Logs", "AWS Managed", "/ecs/nestjs-todo-production", "Centralized stdout/stderr logs, 14 days retention"],
        ["Security IAM Roles", "AWS IAM", "Global / Attached to ECS", "AmazonECSTaskExecutionRolePolicy", "Grants permissions to pull ECR & write logs"],
        ["NoSQL Database", "MongoDB Atlas", "Managed External Cloud", "Whitelisted NAT EIP: 52.57.225.16", "M0 Free Sandbox Cluster, DB: notes_todo"],
        ["CI/CD Pipeline", "GitHub / GitLab", "Cloud Runners (Ubuntu)", "IAM Access Key / Secrets", "1. npm test -> 2. Docker build/push -> 3. ECS deploy"]
    ]

    t = Table(data, colWidths=[130, 95, 150, 160, 245])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A237E")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CFD8DC")),
        ('TOPPADDING', (0, 1), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4.5),
    ]))

    # Wrap table in printable area
    t.wrapOn(c, width, height)
    t.drawOn(c, 30, 85)

    # Add Summary Notes Box below table
    c.setStrokeColor(colors.HexColor("#3F51B5"))
    c.setLineWidth(1)
    c.setFillColor(colors.HexColor("#E8EAF6"))
    c.roundRect(30, 35, width - 60, 42, 4, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor("#1A237E"))
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(40, 62, "Security & Reliability Highlights:")
    c.setFont("Helvetica", 7.5)
    c.drawString(40, 50, "1. Zero Public Exposure: ECS Fargate containers have NO public IP addresses and accept traffic ONLY from the Application Load Balancer Security Group.")
    c.drawString(40, 39, "2. High Availability: Redundant subnets and containers deployed across 2 independent Availability Zones (eu-central-1a & eu-central-1b) with rolling zero-downtime updates.")

    draw_footer(c, width, height, 2, 2)
    c.showPage()
    c.save()
    print("PDF GENERATED SUCCESSFULLY:", filename)

if __name__ == '__main__':
    output_pdf = r"c:\Users\Vlad\Desktop\nestjs-notes-todo-master\aws-architecture.pdf"
    draw_diagram_page(output_pdf)
