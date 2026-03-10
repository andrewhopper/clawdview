---
uuid: cmd-proj-diag-1u2v3w4x
version: 1.0.0
last_updated: 2025-11-11
description: Generate architecture diagrams for prototype
---

# Generate Project Diagram

Generate architecture diagrams (DrawIO + Mermaid) for `{proto_dir}`.

## Usage

```bash
/generate-project-diagram prototypes/proto-027-semantic-schema-mapper [--level=essential] [--output=artifacts/diagrams]
```

**Arguments:**
- `{proto_dir}`: Path to prototype or idea directory
- `--level=essential|all|mermaid|drawio`: Diagram detail level (default: essential)
- `--output=artifacts/diagrams`: Output directory (default: artifacts/diagrams/{proto-name})

**Diagram Levels:**
- `essential`: DrawIO + best Mermaid diagram for project type
- `all`: DrawIO + Mermaid sequence + UML + architecture
- `mermaid`: Only Mermaid diagrams (sequence + UML + architecture)
- `drawio`: Only DrawIO architecture diagram

## Output Files

**Essential level:**
```
artifacts/diagrams/{proto-name}/
├── architecture.drawio    # DrawIO architecture diagram
└── {type}.md              # Best Mermaid diagram (sequence/uml/architecture)
```

**All level:**
```
artifacts/diagrams/{proto-name}/
├── architecture.drawio    # DrawIO architecture diagram
├── sequence.md            # Mermaid sequence diagram
├── uml.md                 # Mermaid UML/class diagram
└── architecture.md        # Mermaid architecture (C4/component)
```

## Workflow

### Step 1: Analyze Project

1. **Read project files**:
   - `.project` file → metadata, tech_stack, description
   - `README.md` → project overview
   - `ARCHITECTURE.md` or `design/ARCHITECTURE.md` → architecture details
   - `src/` → source code structure (if Phase 7-8)

2. **Determine project type**:
   - **API/Backend**: REST API, microservices, backend services
   - **Full-stack**: Frontend + backend + database
   - **Data pipeline**: ETL, data processing, ML workflows
   - **Integration**: Webhook handlers, third-party integrations
   - **CLI/Tool**: Command-line tools, utilities, scripts

3. **Select best Mermaid diagram** for essential level:
   - API/Backend → Sequence diagram (request/response flow)
   - Full-stack → Architecture diagram (C4 context/container)
   - Data pipeline → Flowchart (data flow)
   - Integration → Sequence diagram (integration flow)
   - CLI/Tool → Flowchart (process flow)

### Step 2: Extract Architecture Components

4. **Identify components**:
   - **Services**: API Gateway, Auth Service, Payment Service, etc.
   - **Data stores**: PostgreSQL, Redis, S3, DynamoDB, etc.
   - **External systems**: Third-party APIs, payment processors, etc.
   - **Users/Actors**: End users, admins, systems, etc.
   - **Communication**: HTTP, gRPC, WebSockets, message queues, etc.

5. **Map relationships**:
   - Service dependencies (A calls B)
   - Data flows (A reads/writes to B)
   - Authentication/authorization flows
   - Error handling paths

6. **Extract tech stack**:
   - Frontend: React, Vue, Next.js, etc.
   - Backend: Node.js, Python, Go, etc.
   - Database: PostgreSQL, MongoDB, etc.
   - Infrastructure: AWS, Docker, Kubernetes, etc.

### Step 3: Generate DrawIO Diagram

7. **Create DrawIO XML** (`architecture.drawio`):

**Template:**
```xml
<mxfile host="app.diagrams.net">
  <diagram name="Architecture" id="arch-1">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- User/Actor -->
        <mxCell id="user-1" value="End User" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="60" y="200" width="60" height="120" as="geometry"/>
        </mxCell>

        <!-- Frontend -->
        <mxCell id="frontend-1" value="Frontend&#xa;(React/Next.js)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="200" y="200" width="140" height="80" as="geometry"/>
        </mxCell>

        <!-- API Gateway -->
        <mxCell id="api-1" value="API Gateway&#xa;(Node.js)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="420" y="200" width="140" height="80" as="geometry"/>
        </mxCell>

        <!-- Backend Service -->
        <mxCell id="service-1" value="Service Name&#xa;(Tech)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="640" y="200" width="140" height="80" as="geometry"/>
        </mxCell>

        <!-- Database -->
        <mxCell id="db-1" value="Database&#xa;(PostgreSQL)" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="860" y="190" width="120" height="100" as="geometry"/>
        </mxCell>

        <!-- External System -->
        <mxCell id="ext-1" value="External API" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;dashPattern=8 4;" vertex="1" parent="1">
          <mxGeometry x="640" y="360" width="140" height="80" as="geometry"/>
        </mxCell>

        <!-- Connections -->
        <mxCell id="edge-1" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;fillColor=#dae8fc;strokeColor=#6c8ebf;" edge="1" parent="1" source="user-1" target="frontend-1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-2" value="REST API" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;fillColor=#d5e8d4;strokeColor=#82b366;" edge="1" parent="1" source="frontend-1" target="api-1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-3" value="gRPC" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;strokeWidth=2;fillColor=#d5e8d4;strokeColor=#82b366;" edge="1" parent="1" source="api-1" target="service-1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-4" value="SQL" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;strokeWidth=2;fillColor=#fff2cc;strokeColor=#d6b656;" edge="1" parent="1" source="service-1" target="db-1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="edge-5" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;strokeWidth=2;fillColor=#f8cecc;strokeColor=#b85450;dashed=1;dashPattern=8 4;" edge="1" parent="1" source="service-1" target="ext-1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Layout Strategy:**
- **Horizontal flow**: User → Frontend → Backend → Database (left to right)
- **Vertical grouping**: Layer components vertically when needed
- **Colors**:
  - Blue (#dae8fc): Frontend, client-facing
  - Green (#d5e8d4): Backend services
  - Yellow (#fff2cc): Databases, storage
  - Orange (#ffe6cc): Caches, queues
  - Red (#f8cecc): External systems (dashed border)
- **Shapes**:
  - Rectangle: Services, components
  - Cylinder: Databases
  - Actor: Users
  - Cloud: Cloud services

8. **Customize for project**:
   - Replace generic components with actual project components
   - Use tech stack from `.project` metadata
   - Add all identified relationships
   - Include labels on edges (protocol, data format)

### Step 4: Generate Mermaid Diagrams

9. **Generate Mermaid Sequence Diagram** (`sequence.md`):

**Use for**: API flows, request/response patterns, integration flows

```markdown
# Sequence Diagram: {Project Name}

Generated from: {proto_dir}
Diagram type: Mermaid Sequence
Format: Mermaid

## Visualization

\`\`\`mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API Gateway
    participant Auth Service
    participant Backend Service
    participant Database
    participant External API

    User->>Frontend: Open application
    Frontend->>API Gateway: GET /api/data
    API Gateway->>Auth Service: Validate token
    Auth Service-->>API Gateway: Token valid
    API Gateway->>Backend Service: Fetch data
    Backend Service->>Database: SELECT * FROM table
    Database-->>Backend Service: Return rows
    Backend Service->>External API: Enrich data
    External API-->>Backend Service: Additional info
    Backend Service-->>API Gateway: Processed data
    API Gateway-->>Frontend: JSON response
    Frontend-->>User: Display data
\`\`\`

## Flow Description

**Step 1**: User opens application
**Step 2**: Frontend requests data from API Gateway
**Step 3**: API Gateway validates authentication token
**Step 4**: Backend service fetches data from database
**Step 5**: Backend enriches data with external API
**Step 6**: Response flows back through API Gateway to user

---

*Generated by /generate-project-diagram*
```

10. **Generate Mermaid UML/Class Diagram** (`uml.md`):

**Use for**: Data models, class structures, component relationships

```markdown
# UML Diagram: {Project Name}

Generated from: {proto_dir}
Diagram type: Mermaid UML/Class
Format: Mermaid

## Visualization

\`\`\`mermaid
classDiagram
    class User {
        +String id
        +String email
        +String name
        +Date createdAt
        +login()
        +logout()
    }

    class Order {
        +String id
        +String userId
        +Float total
        +String status
        +Date createdAt
        +create()
        +update()
        +cancel()
    }

    class OrderItem {
        +String id
        +String orderId
        +String productId
        +Integer quantity
        +Float price
    }

    class Product {
        +String id
        +String name
        +String description
        +Float price
        +Integer stock
    }

    User "1" --> "*" Order : places
    Order "1" --> "*" OrderItem : contains
    OrderItem "*" --> "1" Product : references
\`\`\`

## Component Relationships

**User ↔ Order**: One user can place many orders
**Order ↔ OrderItem**: One order contains many items
**OrderItem ↔ Product**: Each item references one product

---

*Generated by /generate-project-diagram*
```

11. **Generate Mermaid Architecture Diagram** (`architecture.md`):

**Use for**: System architecture, component overview, C4 context

```markdown
# Architecture Diagram: {Project Name}

Generated from: {proto_dir}
Diagram type: Mermaid Architecture (C4)
Format: Mermaid

## Visualization

\`\`\`mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile App]
    end

    subgraph "Application Layer"
        C[Frontend - React/Next.js]
        D[API Gateway - Node.js]
    end

    subgraph "Service Layer"
        E[Auth Service]
        F[User Service]
        G[Order Service]
        H[Payment Service]
    end

    subgraph "Data Layer"
        I[(PostgreSQL)]
        J[(Redis Cache)]
        K[S3 Storage]
    end

    subgraph "External Systems"
        L[Payment Processor]
        M[Email Service]
        N[Analytics]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    D --> H
    E --> I
    F --> I
    G --> I
    H --> I
    D --> J
    C --> K
    H --> L
    G --> M
    D --> N
\`\`\`

## Architecture Layers

**Client Layer**: User-facing applications (web, mobile)
**Application Layer**: Frontend + API Gateway (routing, auth)
**Service Layer**: Backend microservices (domain logic)
**Data Layer**: Databases, caches, storage
**External Systems**: Third-party integrations

---

*Generated by /generate-project-diagram*
```

### Step 5: Write Diagram Files

12. **Create output directory**:
    ```bash
    mkdir -p {output_dir}
    ```

13. **Write diagram files**:
    - Use Write tool to create each diagram file
    - Format: DrawIO XML for `.drawio`, Markdown for `.md`

14. **Report results**:

```markdown
# Project Diagrams Generated

**Project**: {proto_name}
**Output**: {output_dir}/
**Level**: {diagram_level}

---

## Files Created

✅ architecture.drawio - DrawIO architecture diagram
{If essential level:}
✅ {type}.md - Mermaid {type} diagram
{If all level:}
✅ sequence.md - Mermaid sequence diagram
✅ uml.md - Mermaid UML/class diagram
✅ architecture.md - Mermaid architecture diagram

---

## Diagram Details

**Project Type**: {API/Full-stack/Data pipeline/Integration/CLI}
**Components Identified**: {count}
**Relationships Mapped**: {count}
**Tech Stack**: {languages, frameworks, databases}

---

## Preview

**DrawIO Architecture**:
- Open in draw.io: https://app.diagrams.net
- File: {output_dir}/architecture.drawio

**Mermaid Diagrams**:
- View on GitHub (auto-renders)
- Files: {output_dir}/*.md

---

✅ Diagrams ready for delivery package
```

## Diagram Selection Logic

**Essential Level** - Select best diagram type:

| Project Type | DrawIO | Best Mermaid |
|-------------|--------|--------------|
| API/Backend | ✅ Architecture | Sequence (request flow) |
| Full-stack | ✅ Architecture | Architecture (C4 context) |
| Data pipeline | ✅ Architecture | Flowchart (data flow) |
| Integration | ✅ Architecture | Sequence (integration flow) |
| CLI/Tool | ✅ Architecture | Flowchart (process flow) |

**All Level** - Generate all diagram types:
- DrawIO: Architecture
- Mermaid: Sequence + UML + Architecture

## Component Detection

**From README.md:**
- Look for "Architecture", "Tech Stack", "Components" sections
- Extract service names, technologies, data stores

**From ARCHITECTURE.md:**
- Comprehensive architecture details
- Component relationships
- Data flows

**From .project:**
- `tech_stack` field → technologies used
- `description` → project purpose

**From src/ directory:**
- Infer services from directory structure
- Detect API endpoints from routes
- Identify data models from schema files

## Tech Stack Icons/Labels

**Frontend:**
- React, Vue, Angular, Next.js, Nuxt.js, Svelte

**Backend:**
- Node.js, Python (Flask/Django), Go, Java (Spring), Ruby (Rails)

**Databases:**
- PostgreSQL, MySQL, MongoDB, DynamoDB, Redis, Cassandra

**Infrastructure:**
- AWS, GCP, Azure, Docker, Kubernetes, Lambda

**Communication:**
- REST, GraphQL, gRPC, WebSockets, MQTT

## Error Handling

**No architecture found:**
```
Warning: No architecture documentation found
Inferring architecture from source code and README...
```

**Insufficient information:**
```
Warning: Limited architecture details available
Generated basic diagram - review and enhance manually
Suggestion: Add ARCHITECTURE.md with component details
```

**Invalid project directory:**
```
Error: Directory not found: {proto_dir}
Check path and try again
```

## Best Practices

1. **Analyze first**: Read all available docs before generating
2. **Be accurate**: Only include components that actually exist
3. **Use labels**: Add protocol/format labels to edges
4. **Color coding**: Consistent colors across all diagrams
5. **Simplify**: Focus on main flow, hide implementation details
6. **Layer properly**: Group related components in subgraphs

## Integration

Works with:
- `/visualize` - Uses similar Mermaid generation logic
- `/prepare-delivery` - Called by main delivery workflow
- DrawIO format compatible with draw.io desktop and web

---

Be accurate, visual, and architecture-focused.
