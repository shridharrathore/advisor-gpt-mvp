# Advisor GPT MVP - Project Plan

## Project Overview
B2B Manufacturing Company chatbot assistant for customer support agents. Provides guided responses with citations for technical troubleshooting, warranty claims, and return policies using RAG with vector database.

## Epic Breakdown (12 Epics)

### **Epic 1: Project Foundation & Setup**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☑ | T1.1 | Initialize project structure | Repo setup, folder structure, README, .gitignore | None |
| ☑ | T1.2 | Setup development environment | Python venv, Node.js, package.json, requirements.txt | T1.1 |
| ☑ | T1.3 | Configure CI/CD pipeline | GitHub Actions, linting, testing workflows | T1.1, T1.2 |

### **Epic 2: Backend Core Infrastructure**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T2.1 | FastAPI application scaffold | Basic FastAPI app, health endpoint, CORS setup | T1.2 |
| ☐ | T2.2 | Database models and schemas | Pydantic models for requests/responses, SQLAlchemy models | T2.1 |
| ☐ | T2.3 | Configuration management | Environment variables, settings class, secrets handling | T2.1 |

### **Epic 3: Vector Database & RAG Setup**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T3.1 | ChromaDB integration | ChromaDB client, collection setup, connection testing | T2.1 |
| ☐ | T3.2 | Document chunking pipeline | chunk_size=800, overlap=120, metadata extraction | T3.1 |
| ☐ | T3.3 | Embedding service | OpenAI embeddings integration, batch processing | T3.1, T2.3 |
| ☐ | T3.4 | RAG retrieval engine | top_k=4, min_score=0.35, similarity search | T3.1, T3.3 |

### **Epic 4: LLM Integration & Response Generation**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T4.1 | OpenAI client setup | GPT integration, prompt templates, token management | T2.3 |
| ☐ | T4.2 | Fixed JSON response format | {answer, steps[], cited_spans[], confidence, disclaimers} | T4.1, T3.4 |
| ☐ | T4.3 | Evidence gate implementation | Minimum confidence threshold, fallback responses | T4.2 |
| ☐ | T4.4 | Response generation pipeline | End-to-end query processing with citations | T4.1, T4.2, T4.3 |

### **Epic 5: Responsible AI & Security**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T5.1 | PII redaction service | Pre-indexing PII detection and removal | T3.2 |
| ☐ | T5.2 | Agent-only access control | Authentication, authorization, role-based access | T2.1 |
| ☐ | T5.3 | Audit logging system | Per-response JSONL logs with version tags | T4.4 |
| ☐ | T5.4 | Fairness and bias checks | Response validation, bias detection | T4.4 |

### **Epic 6: Frontend Core (React)**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T6.1 | React application scaffold | Create React App, routing, basic components | T1.2 |
| ☐ | T6.2 | UI component library | Consistent design system, reusable components | T6.1 |
| ☐ | T6.3 | API client setup | Axios/fetch integration, error handling | T6.1, T2.1 |

### **Epic 7: 3-Pane Agent Workbench UI**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T7.1 | Case/Query pane | Input form, query history, case management | T6.2 |
| ☐ | T7.2 | Draft Answer pane | Response display, edit capabilities, formatting | T6.2, T4.4 |
| ☐ | T7.3 | Evidence pane | Citations display, filters, source documents | T6.2, T3.4 |
| ☐ | T7.4 | Workbench integration | 3-pane layout, responsive design, state management | T7.1, T7.2, T7.3 |

### **Epic 8: Feedback & Interaction Features**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T8.1 | Feedback capture system | Like/dislike buttons, reason selection | T7.2 |
| ☐ | T8.2 | Accept/Edit functionality | Response editing, approval workflow | T7.2 |
| ☐ | T8.3 | Feedback logging | Store feedback in audit logs | T8.1, T8.2, T5.3 |

### **Epic 9: Performance Monitoring & Observability**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T9.1 | Latency tracking | P50/P95 metrics collection from logs | T5.3 |
| ☐ | T9.2 | Performance dashboard | Real-time metrics display for team leads | T9.1, T6.1 |
| ☐ | T9.3 | Daily summary generation | Markdown reports with performance metrics | T9.1 |

### **Epic 10: Testing & Quality Assurance**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T10.1 | Unit tests (Backend) | 80%+ coverage, FastAPI endpoints, RAG pipeline | T4.4 |
| ☐ | T10.2 | Unit tests (Frontend) | Component testing, user interactions | T7.4 |
| ☐ | T10.3 | Integration tests | End-to-end workflows, API integration | T10.1, T10.2 |
| ☐ | T10.4 | Performance tests | Latency validation (P95 < 3s) | T9.1 |

### **Epic 11: Evaluation & Success Metrics**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T11.1 | Retrieval evaluation | retrieval@3 metric implementation | T3.4 |
| ☐ | T11.2 | Groundedness evaluation | ≥95% groundedness validation | T4.4 |
| ☐ | T11.3 | Evaluation pipeline | Automated daily eval runs | T11.1, T11.2 |

### **Epic 12: Deployment & Documentation**
| ✓ | ID | Title | Acceptance Criteria | Dependencies |
|---|----|----|-------------------|--------------|
| ☐ | T12.1 | API documentation | OpenAPI/Swagger docs, endpoint documentation | T4.4 |
| ☐ | T12.2 | User documentation | Agent workbench user guide, troubleshooting | T7.4 |
| ☐ | T12.3 | Deployment configuration | Docker, environment setup, production configs | All epics |
| ☐ | T12.4 | Production deployment | Live system deployment and monitoring | T12.3 |

## Success Criteria
- **Latency**: P95 < 3 seconds
- **Retrieval**: retrieval@3 performance
- **Groundedness**: ≥95% accuracy
- **User Experience**: Clean, consistent, smooth UI/UX

## Technical Constraints
- Max change per task: ≤150 LOC or ≤5 files
- Tests-first development approach
- No new dependencies without approval
- All responses require citations or evidence gate blocking

## RAG Contract Specifications
- **Chunking**: chunk_size=800, overlap=120
- **Retrieval**: top_k=4, min_score=0.35
- **Output Format**: Fixed JSON {answer, steps[], cited_spans[], confidence, disclaimers}
- **Evidence Gate**: Minimum confidence threshold with fallback responses

## Responsible AI Requirements
- Agent-only access (no customer access)
- PII redaction before indexing
- Per-response audit JSONL with version tags
- Fairness and bias validation checks
