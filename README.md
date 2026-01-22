# PPT Comprehension Skill (Pro Max) - 使用指南

本目录包含 **PPT Comprehension Skill** 的实际运行成果。该技能旨在将 PowerPoint 演示文稿转换为 **讲师级 (Lecturer-Level)** 的双语学习指南 (PDF + Markdown)。

不仅是简单的文本提取，它通过 "Pro Max" 级的工作流，能够识别领域（生物学/工程学），并生成深度解析。

---

## 🚀 核心工作流 (Workflow)

该技能遵循严格的 **4步标准化流程**，以确保内容的完整性和深度的专业性。

### 第一步：机械提取 (Extraction)
*   **目标**：从 `.pptx` 源文件中无损提取所有文本结构和高分辨率图片。
*   **工具**：`process_ppt.py` (基于 `python-pptx`, `libreoffice`, `poppler-utils`)
*   **产出**：
    *   `draft.md`：包含原文和图片链接的 Markdown 草稿。
    *   `images/`：所有提取出的图片。
    *   **占位符**：生成 `> [AI: Explain Slide X...]` 供后续 AI 填充。

### 第二步：安全备份 (Preparation)
*   **目标**：建立工作副本，防止后续操作损坏原始提取结果。
*   **操作**：将 `draft.md` 复制为 `study_guide.md`。
*   **原则**：**In-Place Editing**（原位编辑）。我们只修改副本中的占位符，严禁重写整个文件，从而完美保留 PPT 的列表格式和图片布局。

### 第三步：智能解析 (Comprehension - The "Lecturer" Phase)
*   **目标**：AI 扮演领域专家（如生物学教授或风电高级工程师），对每一页 PPT 进行深度讲解。
*   **核心规则**：
    1.  **领域感知**：自动识别是学术理论还是工业实操。
    2.  **严格双语**：关键术语必须保留英文原词（例如：**Solenoid Valve (电磁阀)**）。
    3.  **深度扩展**：不仅仅翻译，而是解释“为什么”和“怎么做”。

### 第四步：成品输出 (Production)
*   **目标**：生成专业排版的 PDF 文档。
*   **工具**：`md2pdf.py` (基于 `WeasyPrint`)
*   **特性**：自动处理 CSS 样式，解决中文排版问题，生成目录。

---

## 🛠️ 调用方法与命令示例

以下是 Agent 在后台执行的具体命令（用户也可在环境配置好的情况下手动运行）：

### 1. 运行提取脚本
```bash
# 语法: python process_ppt.py <输入PPT路径> <输出目录>
uv run --with python-pptx .agent/skills/ppt-comprehension/scripts/process_ppt.py "Deep-Time6(1).pptx" output
```

### 2. 准备工作文件
```bash
cp output/draft.md output/study_guide.md
```

### 3. AI 注入内容 (Agent Action)
*   Agent 读取 `study_guide.md`。
*   Agent 识别占位符 `> [AI: Explain Slide 1...]`。
*   Agent 使用 `multi_replace_file_content` 工具，将占位符替换为 `# 🎓 讲师讲解` 模块。

### 4. 生成 PDF
```bash
# 语法: python md2pdf.py <输入MD文件> <输出PDF文件>
uv run --with Markdown --with weasyprint .agent/skills/ppt-comprehension/scripts/md2pdf.py output/study_guide.md output/study_guide.pdf
```

---

## 📂 案例分析 (Case Studies)

本目录下的两个子目录展示了该技能在不同领域的强大的适应性。

### 案例 A：生物演化 (学术领域)
*   **输入文件**：`Deep-Time6(1).pptx`
*   **输出目录**：`output/`
*   **AI 角色**：大学古生物学讲师
*   **解析特点**：
    *   **理论深度**：详细解释了 **Cope's Law (柯普定律)** 和 **Morphospace (形态空间)** 等抽象概念。
    *   **双语术语**：如 **Goniatite (棱菊石)**, **Sutures (缝合线)**, **Nektonic (游泳生物)**。
    *   **逻辑连贯**：将零散的化石图片串联成完整的演化故事。


## 📄 输出文件说明

在每个输出目录（如 `output/`）中，你会看到：

| 文件名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `draft.md` | 中间文件 | 原始提取的文本和图片链接，不包含 AI 解释。用于回溯比对。 |
| `study_guide.md` | **核心交付物** | 包含完整原文、图片和 **AI 讲师讲解** 的 Markdown 文档。 |
| `study_guide.pdf` | **最终成片** | 格式精美、易于分享和打印的 PDF 版本。 |
| `images/` | 资源文件夹 | 从 PPT 中提取的所有高清图片素材。 |

---


