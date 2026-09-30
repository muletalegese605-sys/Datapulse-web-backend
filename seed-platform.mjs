import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc, doc, setDoc, writeBatch } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAb1Fbs8Y36BZ8rnIUZBjocc-m0Em_PgcQ",
  authDomain: "datapulseapp-20237.firebaseapp.com",
  projectId: "datapulseapp-20237",
  storageBucket: "datapulseapp-20237.firebasestorage.app",
  messagingSenderId: "459433026519",
  appId: "1:459433026519:web:102f1f951bcb91d306e192"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// ============================================
// 1. PLANS (Kaffaltii Sadarkaa)
// ============================================
const plans = [
  { id: "free",       name: "Free",       price_etb: 0,      max_capabilities: 3,  max_records: 1000,    max_users: 2 },
  { id: "starter",    name: "Starter",    price_etb: 1500,   max_capabilities: 10, max_records: 50000,   max_users: 5 },
  { id: "pro",        name: "Pro",        price_etb: 4500,   max_capabilities: 25, max_records: 500000,  max_users: 20 },
  { id: "enterprise", name: "Enterprise", price_etb: 15000,  max_capabilities: 40, max_records: -1,      max_users: -1 }
];

// ============================================
// 2. 40 CAPABILITIES (Gosa Data)
// ============================================
const capabilities = [
  { code: "sales",           name: "Sales Tracking",          category: "Commerce",    min_plan: "free" },
  { code: "inventory",       name: "Inventory Management",    category: "Commerce",    min_plan: "free" },
  { code: "customers",       name: "Customer CRM",            category: "Commerce",    min_plan: "free" },
  { code: "expenses",        name: "Expense Tracking",        category: "Finance",     min_plan: "starter" },
  { code: "invoices",        name: "Invoicing",               category: "Finance",     min_plan: "starter" },
  { code: "payroll",         name: "Payroll Management",      category: "Finance",     min_plan: "pro" },
  { code: "accounting",      name: "Accounting Ledger",       category: "Finance",     min_plan: "pro" },
  { code: "tax_reports",     name: "Tax Reports",             category: "Finance",     min_plan: "pro" },
  { code: "employees",       name: "Employee Directory",      category: "HR",          min_plan: "starter" },
  { code: "attendance",      name: "Attendance Tracking",     category: "HR",          min_plan: "starter" },
  { code: "leave_mgmt",      name: "Leave Management",        category: "HR",          min_plan: "pro" },
  { code: "performance",     name: "Performance Reviews",     category: "HR",          min_plan: "pro" },
  { code: "recruitment",     name: "Recruitment Pipeline",    category: "HR",          min_plan: "enterprise" },
  { code: "projects",        name: "Project Management",      category: "Operations",  min_plan: "starter" },
  { code: "tasks",           name: "Task Tracking",           category: "Operations",  min_plan: "free" },
  { code: "suppliers",       name: "Supplier Management",     category: "Operations",  min_plan: "starter" },
  { code: "purchase_orders", name: "Purchase Orders",         category: "Operations",  min_plan: "pro" },
  { code: "logistics",       name: "Logistics & Shipping",    category: "Operations",  min_plan: "pro" },
  { code: "assets",          name: "Asset Management",        category: "Operations",  min_plan: "enterprise" },
  { code: "contracts",       name: "Contract Management",     category: "Legal",       min_plan: "starter" },
  { code: "compliance",      name: "Compliance Tracking",     category: "Legal",       min_plan: "pro" },
  { code: "audits",          name: "Internal Audits",         category: "Legal",       min_plan: "enterprise" },
  { code: "documents",       name: "Document Vault",          category: "Legal",       min_plan: "starter" },
  { code: "marketing",       name: "Marketing Campaigns",     category: "Marketing",   min_plan: "starter" },
  { code: "leads",           name: "Lead Generation",         category: "Marketing",   min_plan: "free" },
  { code: "social_media",    name: "Social Media Analytics",  category: "Marketing",   min_plan: "pro" },
  { code: "email_campaigns", name: "Email Campaigns",         category: "Marketing",   min_plan: "pro" },
  { code: "seo_analytics",   name: "SEO Analytics",           category: "Marketing",   min_plan: "enterprise" },
  { code: "production",      name: "Production Planning",     category: "Manufacturing", min_plan: "pro" },
  { code: "quality_control", name: "Quality Control",         category: "Manufacturing", min_plan: "pro" },
  { code: "raw_materials",   name: "Raw Material Tracking",   category: "Manufacturing", min_plan: "starter" },
  { code: "maintenance",     name: "Equipment Maintenance",   category: "Manufacturing", min_plan: "enterprise" },
  { code: "analytics",       name: "Business Analytics",      category: "Intelligence", min_plan: "starter" },
  { code: "forecasting",     name: "AI Forecasting",          category: "Intelligence", min_plan: "pro" },
  { code: "dashboards",      name: "Custom Dashboards",       category: "Intelligence", min_plan: "free" },
  { code: "reports",         name: "Automated Reports",       category: "Intelligence", min_plan: "starter" },
  { code: "ai_assistant",    name: "AI Assistant",            category: "Intelligence", min_plan: "pro" },
  { code: "integrations",    name: "Third-Party Integrations", category: "Intelligence", min_plan: "enterprise" },
  { code: "api_access",      name: "REST API Access",         category: "Intelligence", min_plan: "pro" },
  { code: "multi_currency",  name: "Multi-Currency Support",  category: "Intelligence", min_plan: "enterprise" }
];

// ============================================
// 3. SEED FUNCTION
// ============================================
async function seedPlatform() {
  console.log("🚀 Platform seeding jalqabame...\n");

  // Plans
  console.log("📋 Plans galchaa jira...");
  for (const plan of plans) {
    await setDoc(doc(db, "plans", plan.id), plan);
    console.log(`   ✓ Plan: ${plan.name} (ETB ${plan.price_etb})`);
  }

  // Capabilities
  console.log("\n🎯 40 Capabilities galchaa jira...");
  let count = 0;
  for (const cap of capabilities) {
    await setDoc(doc(db, "capabilities", cap.code), cap);
    count++;
    if (count % 10 === 0) console.log(`   ✓ ${count}/40 galameera`);
  }
  console.log(`   ✓ Capabilities ${count} galameera`);

  // Sample Subscriptions (dhaabbilee)
  console.log("\n🏢 Sample Subscriptions galchaa jira...");
  const subscriptions = [
    {
      orgId: "ORG-DEMO",
      plan: "enterprise",
      status: "active",
      price_etb: 15000,
      billing_cycle: "monthly",
      activated_capabilities: capabilities.map(c => c.code), // 40 hunda
      started_at: new Date().toISOString(),
      next_billing: new Date(Date.now() + 30*24*60*60*1000).toISOString()
    },
    {
      orgId: "ORG-STARTER-001",
      plan: "starter",
      status: "active",
      price_etb: 1500,
      billing_cycle: "monthly",
      activated_capabilities: ["sales", "inventory", "customers", "employees", "projects", "tasks", "leads", "dashboards", "reports", "analytics"],
      started_at: new Date().toISOString(),
      next_billing: new Date(Date.now() + 30*24*60*60*1000).toISOString()
    },
    {
      orgId: "ORG-FREE-002",
      plan: "free",
      status: "active",
      price_etb: 0,
      billing_cycle: "monthly",
      activated_capabilities: ["sales", "inventory", "customers"],
      started_at: new Date().toISOString(),
      next_billing: null
    }
  ];

  for (const sub of subscriptions) {
    await setDoc(doc(db, "subscriptions", sub.orgId), sub);
    console.log(`   ✓ ${sub.orgId} → ${sub.plan} (${sub.activated_capabilities.length} caps)`);
  }

  console.log("\n✅ Platform seeding xumurameera!");
  console.log("📊 Summary:");
  console.log(`   • Plans: ${plans.length}`);
  console.log(`   • Capabilities: ${capabilities.length}`);
  console.log(`   • Subscriptions: ${subscriptions.length}`);
}

seedPlatform().catch(console.error);
