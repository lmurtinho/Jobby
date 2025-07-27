// Sample job data for MVP testing and development
// This will be replaced with real job scraping in later iterations

import { Job } from '../types/job';

export const SAMPLE_JOBS: Job[] = [
  {
    id: "1",
    title: "Senior Data Scientist - Remote LATAM",
    company: "TechCorp International",
    location: "Remote (Brazil timezone)",
    salary: "$12,000 - $18,000 USD/month",
    description: "Join our AI team building ML solutions for global markets. We're looking for an experienced data scientist to lead our Brazilian market analysis and develop predictive models for customer behavior.",
    requirements: ["Python", "Machine Learning", "SQL", "TensorFlow", "AWS"],
    posted_date: "2024-01-15",
    apply_url: "https://techcorp.com/careers/senior-data-scientist",
    source: "LinkedIn",
    remote: true
  },
  {
    id: "2", 
    title: "Machine Learning Engineer",
    company: "AI Innovations Brazil",
    location: "São Paulo, SP",
    salary: "R$ 15,000 - R$ 25,000/month",
    description: "Build and deploy ML models at scale. Experience with MLOps, containerization, and cloud platforms required.",
    requirements: ["Python", "Docker", "Kubernetes", "MLOps", "PyTorch"],
    posted_date: "2024-01-14",
    apply_url: "https://aiinnovations.com.br/careers/ml-engineer",
    source: "Indeed",
    remote: false
  },
  {
    id: "3",
    title: "Full Stack Developer - Fintech",
    company: "Brazilian FinTech Solutions", 
    location: "Remote",
    salary: "$8,000 - $12,000 USD/month",
    description: "Join our fintech revolution! Build scalable web applications for financial services using modern React and Node.js stack.",
    requirements: ["React", "Node.js", "TypeScript", "PostgreSQL", "AWS"],
    posted_date: "2024-01-13",
    apply_url: "https://bfintech.com/careers/fullstack",
    source: "AngelList",
    remote: true
  },
  {
    id: "4",
    title: "DevOps Engineer",
    company: "CloudScale Brazil",
    location: "Rio de Janeiro, RJ", 
    salary: "R$ 12,000 - R$ 18,000/month",
    description: "Manage cloud infrastructure and CI/CD pipelines. Experience with AWS, Terraform, and monitoring tools essential.",
    requirements: ["AWS", "Docker", "Terraform", "Kubernetes", "Jenkins"],
    posted_date: "2024-01-12",
    apply_url: "https://cloudscale.com.br/jobs/devops",
    source: "LinkedIn",
    remote: false
  },
  {
    id: "5",
    title: "Python Backend Developer",
    company: "E-commerce Innovations",
    location: "Remote",
    salary: "$6,000 - $10,000 USD/month", 
    description: "Develop high-performance backend services for our e-commerce platform. FastAPI, microservices, and database optimization experience required.",
    requirements: ["Python", "FastAPI", "PostgreSQL", "Redis", "Docker"],
    posted_date: "2024-01-11",
    apply_url: "https://ecommerce-innovations.com/careers/backend",
    source: "Stack Overflow Jobs",
    remote: true
  },
  {
    id: "6",
    title: "Data Analytics Manager", 
    company: "RetailTech Solutions",
    location: "Belo Horizonte, MG",
    salary: "R$ 18,000 - R$ 28,000/month",
    description: "Lead a team of data analysts to drive business insights. Experience with SQL, Python, and business intelligence tools required.",
    requirements: ["SQL", "Python", "Tableau", "Team Leadership", "Statistics"],
    posted_date: "2024-01-10",
    apply_url: "https://retailtech.com.br/careers/analytics-manager",
    source: "Indeed",
    remote: false
  },
  {
    id: "7",
    title: "React Frontend Developer",
    company: "SaaS Startup Brazil",
    location: "Remote",
    salary: "$7,000 - $11,000 USD/month",
    description: "Build beautiful, responsive user interfaces for our SaaS platform. Strong React, TypeScript, and modern CSS skills required.",
    requirements: ["React", "TypeScript", "CSS3", "JavaScript", "Git"],
    posted_date: "2024-01-09", 
    apply_url: "https://saasstartup.com.br/jobs/frontend",
    source: "AngelList",
    remote: true
  },
  {
    id: "8",
    title: "Senior Software Engineer",
    company: "Enterprise Solutions Inc",
    location: "São Paulo, SP",
    salary: "R$ 25,000 - R$ 35,000/month",
    description: "Design and implement large-scale software architectures. 8+ years experience with distributed systems and microservices required.",
    requirements: ["Java", "Spring Boot", "Microservices", "System Design", "Leadership"],
    posted_date: "2024-01-08",
    apply_url: "https://enterprise-solutions.com/careers/architect",
    source: "LinkedIn",
    remote: false
  },
  {
    id: "9",
    title: "QA Automation Engineer",
    company: "Quality First Tech",
    location: "Remote",
    salary: "$5,000 - $8,000 USD/month",
    description: "Build automated testing frameworks and ensure product quality. Experience with Selenium, Cypress, and CI/CD integration required.",
    requirements: ["Selenium", "Cypress", "JavaScript", "Jenkins", "API Testing"],
    posted_date: "2024-01-07",
    apply_url: "https://qualityfirst.com/careers/qa-automation",
    source: "Stack Overflow Jobs", 
    remote: true
  },
  {
    id: "10",
    title: "Cloud Solutions Engineer",
    company: "AWS Partner Brazil",
    location: "Brasília, DF",
    salary: "R$ 14,000 - R$ 22,000/month",
    description: "Help enterprises migrate to cloud. Strong AWS knowledge and customer-facing experience essential.",
    requirements: ["AWS", "Cloud Architecture", "Consulting", "Networking", "Security"],
    posted_date: "2024-01-06",
    apply_url: "https://awspartner.com.br/jobs/cloud-engineer",
    source: "Indeed",
    remote: false
  },
  {
    id: "11",
    title: "Senior Product Manager",
    company: "Digital Innovation Labs",
    location: "São Paulo, SP",
    salary: "R$ 20,000 - R$ 30,000/month",
    description: "Lead product strategy and roadmap for our digital transformation initiatives. Work closely with engineering, design, and business teams to deliver user-centered solutions.",
    requirements: ["Product Strategy", "User Research", "Data Analysis", "Agile", "Leadership"],
    posted_date: "2024-01-05",
    apply_url: "https://digitalinnovation.com.br/careers/product-manager",
    source: "LinkedIn",
    remote: false
  },
  {
    id: "12",
    title: "Cybersecurity Analyst",
    company: "SecureBank Brasil",
    location: "Brasília, DF",
    salary: "R$ 12,000 - R$ 18,000/month",
    description: "Protect our financial infrastructure from cyber threats. Monitor security events, conduct vulnerability assessments, and implement security protocols.",
    requirements: ["Information Security", "Penetration Testing", "CISSP", "Python", "Network Security"],
    posted_date: "2024-01-12",
    apply_url: "https://securebank.com.br/careers/cybersecurity",
    source: "Indeed",
    remote: false
  },
  {
    id: "13",
    title: "UX/UI Designer",
    company: "Design Studio Tropical",
    location: "Remote",
    salary: "$6,000 - $10,000 USD/month",
    description: "Create beautiful and intuitive user experiences for mobile and web applications. Collaborate with product teams to design user-centered solutions.",
    requirements: ["Figma", "User Research", "Prototyping", "Design Systems", "Adobe Creative Suite"],
    posted_date: "2024-01-11",
    apply_url: "https://tropicaldesign.com/careers/ux-designer",
    source: "Dribbble",
    remote: true
  },
  {
    id: "14",
    title: "Blockchain Developer",
    company: "CryptoBR Solutions",
    location: "Remote",
    salary: "$15,000 - $25,000 USD/month",
    description: "Develop smart contracts and DeFi applications on Ethereum and Polygon networks. Experience with Solidity and Web3 technologies required.",
    requirements: ["Solidity", "Web3", "Ethereum", "Smart Contracts", "JavaScript"],
    posted_date: "2024-01-10",
    apply_url: "https://cryptobr.com/careers/blockchain-dev",
    source: "CryptoJobs",
    remote: true
  },
  {
    id: "15",
    title: "Sales Development Representative",
    company: "SaaS Brasil",
    location: "São Paulo, SP",
    salary: "R$ 8,000 - R$ 15,000/month + commission",
    description: "Generate qualified leads for our B2B SaaS platform. Work with marketing team to identify prospects and convert them into sales opportunities.",
    requirements: ["B2B Sales", "CRM", "Lead Generation", "Communication", "English"],
    posted_date: "2024-01-09",
    apply_url: "https://saasbrasil.com/careers/sdr",
    source: "LinkedIn",
    remote: false
  },
  {
    id: "16",
    title: "iOS Developer",
    company: "Mobile First Apps",
    location: "Remote",
    salary: "R$ 14,000 - R$ 22,000/month",
    description: "Build native iOS applications using Swift and SwiftUI. Focus on performance optimization and user experience for consumer apps.",
    requirements: ["Swift", "SwiftUI", "iOS SDK", "Core Data", "Git"],
    posted_date: "2024-01-08",
    apply_url: "https://mobilefirst.com.br/careers/ios",
    source: "Stack Overflow",
    remote: true
  },
  {
    id: "17",
    title: "Digital Marketing Manager",
    company: "Growth Hackers BR",
    location: "Rio de Janeiro, RJ",
    salary: "R$ 10,000 - R$ 16,000/month",
    description: "Lead digital marketing campaigns across multiple channels. Manage SEO, SEM, social media, and content marketing strategies.",
    requirements: ["Digital Marketing", "SEO", "Google Ads", "Analytics", "Content Strategy"],
    posted_date: "2024-01-07",
    apply_url: "https://growthhackers.com.br/careers/marketing",
    source: "Indeed",
    remote: false
  },
  {
    id: "18",
    title: "Cloud Solutions Architect",
    company: "AWS Partner Brazil",
    location: "São Paulo, SP",
    salary: "$18,000 - $28,000 USD/month",
    description: "Design and implement cloud-native solutions for enterprise clients. Lead cloud migration projects and optimize infrastructure costs.",
    requirements: ["AWS", "Cloud Architecture", "Terraform", "Kubernetes", "Python"],
    posted_date: "2024-01-06",
    apply_url: "https://awspartner.com.br/careers/architect",
    source: "AWS Jobs",
    remote: false
  },
  {
    id: "19",
    title: "Frontend Developer - React",
    company: "WebDev Solutions",
    location: "Remote",
    salary: "R$ 12,000 - R$ 18,000/month",
    description: "Build modern web applications using React, TypeScript, and Next.js. Focus on performance, accessibility, and responsive design.",
    requirements: ["React", "TypeScript", "Next.js", "CSS", "Testing"],
    posted_date: "2024-01-05",
    apply_url: "https://webdevsolutions.com.br/careers/frontend",
    source: "GitHub Jobs",
    remote: true
  },
  {
    id: "20",
    title: "Data Analyst - E-commerce",
    company: "RetailTech Brasil",
    location: "Belo Horizonte, MG",
    salary: "R$ 9,000 - R$ 14,000/month",
    description: "Analyze customer behavior and sales data to drive business decisions. Create dashboards and reports for stakeholders.",
    requirements: ["SQL", "Power BI", "Excel", "Statistics", "E-commerce"],
    posted_date: "2024-01-04",
    apply_url: "https://retailtech.com.br/careers/analyst",
    source: "Glassdoor",
    remote: false
  },
  {
    id: "21",
    title: "Backend Developer - Java",
    company: "Enterprise Systems Ltd",
    location: "Curitiba, PR",
    salary: "R$ 13,000 - R$ 20,000/month",
    description: "Develop enterprise-grade backend systems using Java Spring framework. Work on microservices architecture and API development.",
    requirements: ["Java", "Spring Boot", "Microservices", "PostgreSQL", "REST APIs"],
    posted_date: "2024-01-03",
    apply_url: "https://enterprisesystems.com.br/careers/java",
    source: "Indeed",
    remote: false
  },
  {
    id: "22",
    title: "QA Engineer - Automation",
    company: "QualityFirst Testing",
    location: "Remote",
    salary: "$8,000 - $12,000 USD/month",
    description: "Design and implement automated testing frameworks. Ensure quality across web and mobile applications through comprehensive testing strategies.",
    requirements: ["Test Automation", "Selenium", "Cypress", "Python", "CI/CD"],
    posted_date: "2024-01-02",
    apply_url: "https://qualityfirst.com/careers/qa",
    source: "TestingJobs",
    remote: true
  },
  {
    id: "23",
    title: "Content Writer - Tech",
    company: "TechContent Pro",
    location: "Remote",
    salary: "R$ 6,000 - R$ 10,000/month",
    description: "Create engaging technical content for blogs, documentation, and marketing materials. Focus on software development and technology topics.",
    requirements: ["Technical Writing", "SEO", "Content Strategy", "Technology", "English"],
    posted_date: "2024-01-01",
    apply_url: "https://techcontent.pro/careers/writer",
    source: "ContentJobs",
    remote: true
  },
  {
    id: "24",
    title: "AI Research Scientist",
    company: "AI Lab Brasil",
    location: "São Paulo, SP",
    salary: "$20,000 - $35,000 USD/month",
    description: "Conduct cutting-edge research in machine learning and artificial intelligence. Publish papers and develop novel algorithms for computer vision and NLP.",
    requirements: ["PhD in AI/ML", "Research", "PyTorch", "Computer Vision", "NLP"],
    posted_date: "2023-12-31",
    apply_url: "https://ailab.com.br/careers/researcher",
    source: "Academic Jobs",
    remote: false
  },
  {
    id: "25",
    title: "Scrum Master",
    company: "Agile Solutions BR",
    location: "Porto Alegre, RS",
    salary: "R$ 11,000 - R$ 17,000/month",
    description: "Facilitate agile ceremonies and coach development teams. Remove impediments and ensure smooth delivery of software products.",
    requirements: ["Scrum", "Agile Coaching", "Jira", "Confluence", "Leadership"],
    posted_date: "2023-12-30",
    apply_url: "https://agilesolutions.com.br/careers/scrum-master",
    source: "LinkedIn",
    remote: false
  },
  {
    id: "26",
    title: "Game Developer - Unity",
    company: "Indie Games Studio",
    location: "Remote",
    salary: "R$ 10,000 - R$ 16,000/month",
    description: "Develop mobile and PC games using Unity engine. Work on gameplay mechanics, physics, and user interface systems.",
    requirements: ["Unity", "C#", "Game Design", "3D Graphics", "Mobile Development"],
    posted_date: "2023-12-29",
    apply_url: "https://indiegames.com.br/careers/unity-dev",
    source: "GameDev Jobs",
    remote: true
  },
  {
    id: "27",
    title: "Business Analyst - Fintech",
    company: "PaymentTech Solutions",
    location: "São Paulo, SP",
    salary: "R$ 9,500 - R$ 15,000/month",
    description: "Analyze business requirements for payment processing systems. Bridge the gap between business stakeholders and technical teams.",
    requirements: ["Business Analysis", "Requirements Gathering", "Process Mapping", "Fintech", "SQL"],
    posted_date: "2023-12-28",
    apply_url: "https://paymenttech.com.br/careers/ba",
    source: "Indeed",
    remote: false
  },
  {
    id: "28",
    title: "Ruby on Rails Developer",
    company: "Rails Masters",
    location: "Remote",
    salary: "$10,000 - $16,000 USD/month",
    description: "Build and maintain Ruby on Rails applications. Work on legacy system modernization and new feature development.",
    requirements: ["Ruby on Rails", "PostgreSQL", "Redis", "Sidekiq", "TDD"],
    posted_date: "2023-12-27",
    apply_url: "https://railsmasters.com/careers/rails-dev",
    source: "Ruby Jobs",
    remote: true
  },
  {
    id: "29",
    title: "Network Engineer",
    company: "Infrastructure Pro",
    location: "Brasília, DF",
    salary: "R$ 12,000 - R$ 19,000/month",
    description: "Design and maintain enterprise network infrastructure. Implement security protocols and optimize network performance.",
    requirements: ["Networking", "Cisco", "Firewall", "VPN", "Network Security"],
    posted_date: "2023-12-26",
    apply_url: "https://infrastructurepro.com.br/careers/network",
    source: "TechJobs",
    remote: false
  },
  {
    id: "30",
    title: "Technical Writer",
    company: "Documentation Experts",
    location: "Remote",
    salary: "R$ 7,000 - R$ 12,000/month",
    description: "Create comprehensive technical documentation for software products. Work with engineering teams to document APIs and user guides.",
    requirements: ["Technical Writing", "API Documentation", "Markdown", "Git", "Software Documentation"],
    posted_date: "2023-12-25",
    apply_url: "https://docexperts.com/careers/tech-writer",
    source: "WriterJobs",
    remote: true
  },
  {
    id: "31",
    title: "Android Developer",
    company: "Mobile Innovation Labs",
    location: "Rio de Janeiro, RJ",
    salary: "R$ 13,000 - R$ 20,000/month",
    description: "Develop native Android applications using Kotlin and Jetpack Compose. Focus on performance optimization and modern Android development practices.",
    requirements: ["Kotlin", "Android SDK", "Jetpack Compose", "MVVM", "Room Database"],
    posted_date: "2023-12-24",
    apply_url: "https://mobilelabs.com.br/careers/android",
    source: "Android Jobs",
    remote: false
  },
  {
    id: "32",
    title: "Database Administrator",
    company: "DataOps Solutions",
    location: "São Paulo, SP",
    salary: "R$ 14,000 - R$ 22,000/month",
    description: "Manage and optimize database systems for high-performance applications. Ensure data integrity, backup strategies, and disaster recovery.",
    requirements: ["PostgreSQL", "MySQL", "Database Optimization", "Backup Strategies", "SQL Tuning"],
    posted_date: "2023-12-23",
    apply_url: "https://dataops.com.br/careers/dba",
    source: "Database Jobs",
    remote: false
  },
  {
    id: "33",
    title: "SEO Specialist",
    company: "Digital Growth Agency",
    location: "Remote",
    salary: "R$ 6,000 - R$ 11,000/month",
    description: "Optimize websites for search engines and improve organic traffic. Conduct keyword research, technical SEO audits, and content optimization.",
    requirements: ["SEO", "Google Analytics", "Keyword Research", "Technical SEO", "Content Marketing"],
    posted_date: "2023-12-22",
    apply_url: "https://digitalgrowth.com.br/careers/seo",
    source: "Marketing Jobs",
    remote: true
  },
  {
    id: "34",
    title: "Solutions Engineer",
    company: "TechSales Pro",
    location: "São Paulo, SP",
    salary: "R$ 15,000 - R$ 25,000/month + commission",
    description: "Provide technical expertise in the sales process. Demonstrate product capabilities and design solutions for enterprise customers.",
    requirements: ["Technical Sales", "Solution Design", "Customer Engagement", "Presentation Skills", "Technology"],
    posted_date: "2023-12-21",
    apply_url: "https://techsales.pro/careers/solutions",
    source: "Sales Jobs",
    remote: false
  },
  {
    id: "35",
    title: "Flutter Developer",
    company: "Cross Platform Apps",
    location: "Remote",
    salary: "R$ 11,000 - R$ 18,000/month",
    description: "Build cross-platform mobile applications using Flutter and Dart. Focus on creating smooth user experiences across iOS and Android.",
    requirements: ["Flutter", "Dart", "Mobile Development", "State Management", "Firebase"],
    posted_date: "2023-12-20",
    apply_url: "https://crossplatform.com.br/careers/flutter",
    source: "Flutter Jobs",
    remote: true
  },
  {
    id: "36",
    title: "HR Business Partner",
    company: "People First Company",
    location: "Belo Horizonte, MG",
    salary: "R$ 10,000 - R$ 16,000/month",
    description: "Partner with business leaders to align HR strategy with business objectives. Manage talent acquisition, performance management, and employee development.",
    requirements: ["HR Strategy", "Talent Acquisition", "Performance Management", "Employee Relations", "Psychology"],
    posted_date: "2023-12-19",
    apply_url: "https://peoplefirst.com.br/careers/hr-bp",
    source: "HR Jobs",
    remote: false
  },
  {
    id: "37",
    title: "Data Engineer - Big Data",
    company: "BigData Brasil",
    location: "São Paulo, SP",
    salary: "R$ 16,000 - R$ 25,000/month",
    description: "Design and build data pipelines for large-scale data processing. Work with Spark, Kafka, and cloud data platforms.",
    requirements: ["Apache Spark", "Kafka", "Data Pipeline", "Scala", "AWS/GCP"],
    posted_date: "2023-12-18",
    apply_url: "https://bigdata.com.br/careers/data-engineer",
    source: "Data Jobs",
    remote: false
  },
  {
    id: "38",
    title: "Customer Success Manager",
    company: "SaaS Success Co",
    location: "Remote",
    salary: "R$ 9,000 - R$ 15,000/month",
    description: "Ensure customer success and retention for our SaaS platform. Manage onboarding, training, and ongoing customer relationships.",
    requirements: ["Customer Success", "Account Management", "SaaS", "Communication", "Analytics"],
    posted_date: "2023-12-17",
    apply_url: "https://saassuccess.com/careers/csm",
    source: "Customer Success Jobs",
    remote: true
  },
  {
    id: "39",
    title: "Site Reliability Engineer",
    company: "Reliable Systems",
    location: "Rio de Janeiro, RJ",
    salary: "$14,000 - $22,000 USD/month",
    description: "Ensure system reliability and performance at scale. Implement monitoring, alerting, and incident response procedures.",
    requirements: ["SRE", "Monitoring", "Kubernetes", "Prometheus", "Incident Response"],
    posted_date: "2023-12-16",
    apply_url: "https://reliablesystems.com.br/careers/sre",
    source: "SRE Jobs",
    remote: false
  },
  {
    id: "40",
    title: "E-commerce Manager",
    company: "Online Retail Hub",
    location: "Curitiba, PR",
    salary: "R$ 8,000 - R$ 14,000/month",
    description: "Manage e-commerce operations including product catalog, pricing strategy, and online marketing campaigns.",
    requirements: ["E-commerce", "Digital Marketing", "Analytics", "Project Management", "Marketplace"],
    posted_date: "2023-12-15",
    apply_url: "https://retailhub.com.br/careers/ecommerce",
    source: "Retail Jobs",
    remote: false
  },
  {
    id: "41",
    title: "Go Developer",
    company: "Modern Backend Systems",
    location: "Remote",
    salary: "$12,000 - $20,000 USD/month",
    description: "Build high-performance backend services using Go. Work on microservices architecture and distributed systems.",
    requirements: ["Go", "Microservices", "gRPC", "Docker", "Distributed Systems"],
    posted_date: "2023-12-14",
    apply_url: "https://modernbackend.com/careers/go-dev",
    source: "Go Jobs",
    remote: true
  },
  {
    id: "42",
    title: "Financial Analyst - Tech",
    company: "FinTech Analytics",
    location: "São Paulo, SP",
    salary: "R$ 10,000 - R$ 16,000/month",
    description: "Analyze financial performance of technology companies. Prepare financial models, forecasts, and investment recommendations.",
    requirements: ["Financial Analysis", "Excel", "Financial Modeling", "Technology Sector", "Valuation"],
    posted_date: "2023-12-13",
    apply_url: "https://fintechanalytics.com.br/careers/analyst",
    source: "Finance Jobs",
    remote: false
  },
  {
    id: "43",
    title: "Technical Support Engineer",
    company: "SupportTech Solutions",
    location: "Remote",
    salary: "R$ 7,000 - R$ 12,000/month",
    description: "Provide technical support for software products. Troubleshoot issues, create documentation, and work with engineering teams.",
    requirements: ["Technical Support", "Troubleshooting", "Customer Service", "Documentation", "Linux"],
    posted_date: "2023-12-12",
    apply_url: "https://supporttech.com.br/careers/support",
    source: "Support Jobs",
    remote: true
  },
  {
    id: "44",
    title: "Graphic Designer",
    company: "Creative Studio BR",
    location: "Rio de Janeiro, RJ",
    salary: "R$ 5,000 - R$ 9,000/month",
    description: "Create visual designs for digital and print media. Work on branding, marketing materials, and web graphics.",
    requirements: ["Adobe Creative Suite", "Graphic Design", "Branding", "Typography", "Print Design"],
    posted_date: "2023-12-11",
    apply_url: "https://creativestudio.com.br/careers/designer",
    source: "Design Jobs",
    remote: false
  },
  {
    id: "45",
    title: "Python Developer - Web",
    company: "WebPython Solutions",
    location: "Remote",
    salary: "R$ 11,000 - R$ 17,000/month",
    description: "Develop web applications using Python and Django framework. Focus on scalable architecture and clean code practices.",
    requirements: ["Python", "Django", "REST APIs", "PostgreSQL", "Git"],
    posted_date: "2023-12-10",
    apply_url: "https://webpython.com.br/careers/python-dev",
    source: "Python Jobs",
    remote: true
  },
  {
    id: "46",
    title: "Operations Manager - Tech",
    company: "TechOps Brasil",
    location: "Brasília, DF",
    salary: "R$ 12,000 - R$ 20,000/month",
    description: "Manage day-to-day operations of technology teams. Optimize processes, coordinate projects, and ensure efficient delivery.",
    requirements: ["Operations Management", "Process Optimization", "Project Coordination", "Team Leadership", "Technology"],
    posted_date: "2023-12-09",
    apply_url: "https://techops.com.br/careers/ops-manager",
    source: "Management Jobs",
    remote: false
  },
  {
    id: "47",
    title: "Penetration Tester",
    company: "CyberSec Experts",
    location: "São Paulo, SP",
    salary: "R$ 15,000 - R$ 25,000/month",
    description: "Conduct security assessments and penetration testing. Identify vulnerabilities and provide recommendations for security improvements.",
    requirements: ["Penetration Testing", "Ethical Hacking", "Security Assessment", "Kali Linux", "OSCP"],
    posted_date: "2023-12-08",
    apply_url: "https://cybersec.com.br/careers/pentest",
    source: "Security Jobs",
    remote: false
  },
  {
    id: "48",
    title: "Video Editor",
    company: "Media Production House",
    location: "Remote",
    salary: "R$ 6,000 - R$ 11,000/month",
    description: "Edit video content for social media, marketing campaigns, and educational materials. Work with motion graphics and sound design.",
    requirements: ["Video Editing", "Adobe Premiere", "After Effects", "Motion Graphics", "Sound Design"],
    posted_date: "2023-12-07",
    apply_url: "https://mediaproduction.com.br/careers/editor",
    source: "Media Jobs",
    remote: true
  },
  {
    id: "49",
    title: "Rust Developer",
    company: "Systems Programming Co",
    location: "Remote",
    salary: "$15,000 - $25,000 USD/month",
    description: "Develop high-performance systems software using Rust. Work on compiler technology, operating systems, and blockchain projects.",
    requirements: ["Rust", "Systems Programming", "Performance Optimization", "Concurrency", "Low-level Programming"],
    posted_date: "2023-12-06",
    apply_url: "https://systemsprog.com/careers/rust-dev",
    source: "Rust Jobs",
    remote: true
  },
  {
    id: "50",
    title: "Legal Counsel - Tech",
    company: "LegalTech Advisors",
    location: "São Paulo, SP",
    salary: "R$ 18,000 - R$ 30,000/month",
    description: "Provide legal guidance for technology companies. Handle contract negotiations, intellectual property, and regulatory compliance.",
    requirements: ["Law Degree", "Technology Law", "Contract Negotiation", "IP Law", "Regulatory Compliance"],
    posted_date: "2023-12-05",
    apply_url: "https://legaltech.com.br/careers/counsel",
    source: "Legal Jobs",
    remote: false
  }
];

// Helper functions for working with sample job data
export const getJobById = (id: string): Job | undefined => {
  return SAMPLE_JOBS.find(job => job.id === id);
};

export const getJobsByCompany = (company: string): Job[] => {
  return SAMPLE_JOBS.filter(job => 
    job.company.toLowerCase().includes(company.toLowerCase())
  );
};

export const getRemoteJobs = (): Job[] => {
  return SAMPLE_JOBS.filter(job => job.remote);
};

export const getJobsByLocation = (location: string): Job[] => {
  return SAMPLE_JOBS.filter(job =>
    job.location.toLowerCase().includes(location.toLowerCase())
  );
};

export const getJobsBySkill = (skill: string): Job[] => {
  return SAMPLE_JOBS.filter(job =>
    job.requirements.some(req => 
      req.toLowerCase().includes(skill.toLowerCase())
    )
  );
};

// Export count for testing
export const SAMPLE_JOBS_COUNT = SAMPLE_JOBS.length;
