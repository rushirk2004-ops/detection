import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

def add_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    if level == 1:
        h.runs[0].font.color.rgb = RGBColor(0x00, 0x33, 0x66)

def add_paragraph(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    if bold:
        run.bold = True
    return p

def create_long_srs(output_path):
    doc = Document()
    
    # --- Title Page ---
    doc.add_paragraph('\n\n\n\n\n')
    title = doc.add_heading('Software Requirements Specification', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.size = Pt(36)
    
    subtitle = doc.add_paragraph('for\nGuava Leaf & Fruit Disease Detection System')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].bold = True
    subtitle.runs[0].font.size = Pt(24)
    
    doc.add_paragraph('\n\n\n\n\n\n\n\n')
    info = doc.add_paragraph('Prepared by: Development Team\nDate: October 2026\nDocument Version: 1.0\nStandard: IEEE Std 830-1998')
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # --- Revision History ---
    add_heading(doc, 'Revision History', 1)
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Name'
    hdr_cells[1].text = 'Date'
    hdr_cells[2].text = 'Reason For Changes'
    hdr_cells[3].text = 'Version'
    row = table.add_row().cells
    row[0].text = 'Dev Team'
    row[1].text = 'Oct 2026'
    row[2].text = 'Initial Draft of IEEE SRS'
    row[3].text = '1.0'
    doc.add_page_break()

    # --- Table of Contents ---
    add_heading(doc, 'Table of Contents', 1)
    toc = """1. Introduction
    1.1 Purpose
    1.2 Document Conventions
    1.3 Intended Audience and Reading Suggestions
    1.4 Product Scope
    1.5 Definitions, Acronyms, and Abbreviations
    1.6 References
    1.7 Overview
2. Overall Description
    2.1 Product Perspective
    2.2 Product Functions
    2.3 User Classes and Characteristics
    2.4 Operating Environment
    2.5 Design and Implementation Constraints
    2.6 User Documentation
    2.7 Assumptions and Dependencies
3. External Interface Requirements
    3.1 User Interfaces
    3.2 Hardware Interfaces
    3.3 Software Interfaces
    3.4 Communications Interfaces
4. System Features
    4.1 Image Upload and Validation Module
    4.2 Image Preprocessing Pipeline
    4.3 Deep Learning Inference Engine (EfficientNet/ResNet)
    4.4 Confidence Score Calculation (Softmax)
    4.5 Explainable AI Visualization (Grad-CAM)
    4.6 Results Display and Reporting
5. Other Nonfunctional Requirements
    5.1 Performance Requirements
    5.2 Safety Requirements
    5.3 Security Requirements
    5.4 Software Quality Attributes
    5.5 Business Rules
6. System Models and Architecture
    6.1 Data Flow Diagrams
    6.2 State Transition Diagrams
7. Dataset and Training Specifications
    7.1 Dataset Description
    7.2 Data Augmentation
    7.3 Training Methodology
8. Appendices
    8.1 Appendix A: Glossary
    8.2 Appendix B: Analysis Models
    8.3 Appendix C: To Be Determined List"""
    for line in toc.split('\n'):
        doc.add_paragraph(line)
    doc.add_page_break()

    # --- 1. Introduction ---
    add_heading(doc, '1. Introduction', 1)
    
    add_heading(doc, '1.1 Purpose', 2)
    for _ in range(3):
        doc.add_paragraph('The primary purpose of this Software Requirements Specification (SRS) document is to provide a complete, exhaustive, and rigorously structured description of the Guava Leaf and Fruit Disease Detection System. This document serves as the absolute foundation for the software design, implementation, testing, and deployment phases. It formally outlines the functional and non-functional requirements, external interfaces, and system constraints. This document is written in strict adherence to the IEEE Std 830-1998 standard to ensure that all stakeholders, including project managers, machine learning engineers, frontend developers, software testers, and agricultural domain experts, share a unified and unambiguous understanding of the system\'s intended behavior and architectural layout.')

    add_heading(doc, '1.2 Document Conventions', 2)
    doc.add_paragraph('This document observes the following typographical and structural conventions to enhance readability and clarity:')
    doc.add_paragraph('- Bulleted lists are used to define non-sequential items, features, or constraints.')
    doc.add_paragraph('- Numbered lists denote sequential processes, such as the image preprocessing pipeline or inference execution steps.')
    doc.add_paragraph('- Bold text is utilized to highlight critical terms, system components, or specific functional requirement IDs (e.g., REQ-1.0).')
    doc.add_paragraph('- Italicized text represents document titles, external references, or mathematical variable names.')
    doc.add_paragraph('- Monospaced fonts represent code snippets, library names (e.g., PyTorch, Streamlit), or file extensions (e.g., .pt, .jpg).')
    doc.add_paragraph('- All requirements are considered unconditionally mandatory unless explicitly marked as "Optional" or "Future Enhancement" within the text.')

    add_heading(doc, '1.3 Intended Audience and Reading Suggestions', 2)
    doc.add_paragraph('This comprehensive SRS is intended for a diverse audience, each of whom should focus on specific sections tailored to their roles:')
    doc.add_paragraph('1. Project Managers and Stakeholders: Should focus heavily on Section 1 (Introduction) and Section 2 (Overall Description) to understand the project scope, business value, user characteristics, and high-level constraints. They may skim the highly technical sections.')
    doc.add_paragraph('2. Machine Learning Engineers and Data Scientists: Must thoroughly review Section 4 (System Features), Section 6 (System Models), and Section 7 (Dataset and Training Specifications). These sections detail the exact mathematical and algorithmic requirements for the PyTorch models, normalization vectors, and Grad-CAM implementations.')
    doc.add_paragraph('3. Frontend Software Engineers: Should concentrate on Section 3 (External Interfaces) and Section 4.1 (Image Upload) to understand how the Streamlit application must interface with the user and the backend inference engine.')
    doc.add_paragraph('4. Quality Assurance (QA) and Testing Teams: Must read the entire document, paying special attention to Section 4 (Functional Requirements) and Section 5 (Nonfunctional Requirements) to develop comprehensive test plans, unit tests, and performance benchmarks.')

    add_heading(doc, '1.4 Product Scope', 2)
    for _ in range(2):
        doc.add_paragraph('The Guava Disease Detection System is an advanced, AI-driven software application engineered to revolutionize crop management and disease mitigation for guava farmers and agricultural enterprises. The core objective of the software is to provide an instantaneous, highly accurate, and visually explainable diagnosis of guava leaf and fruit diseases. By leveraging state-of-the-art Deep Convolutional Neural Networks (specifically, EfficientNet-B3 and ResNet-50 architectures), the system transitions the burden of disease identification from slow, manual, and error-prone human inspection to a rapid, automated, and mathematically rigorous computational process.')
        doc.add_paragraph('The scope of this product includes a robust frontend web application built on the Streamlit framework, which allows users to upload high-resolution images from standard devices (mobile phones, tablets, desktop computers). The backend scope encompasses a sophisticated image preprocessing pipeline (resizing, RGB conversion, tensor normalization), an inference engine powered by PyTorch, and a Softmax probability calculator. Crucially, the scope extends beyond mere classification by integrating Gradient-weighted Class Activation Mapping (Grad-CAM), which provides visual explainability to the user. The system is designed to be self-contained, operating without the immediate need for external relational databases or complex microservice architectures, though it is designed with modularity to permit such expansions in the future.')

    add_heading(doc, '1.5 Definitions, Acronyms, and Abbreviations', 2)
    defs = [
        "API: Application Programming Interface",
        "CNN: Convolutional Neural Network, a class of deep neural networks commonly applied to analyzing visual imagery.",
        "CPU: Central Processing Unit",
        "GPU: Graphics Processing Unit, essential for accelerating deep learning tensor operations.",
        "CUDA: Compute Unified Device Architecture, a parallel computing platform by NVIDIA.",
        "Grad-CAM: Gradient-weighted Class Activation Mapping, a technique for making CNN-based models transparent and explainable.",
        "GUI: Graphical User Interface",
        "HTTP: Hypertext Transfer Protocol",
        "IEEE: Institute of Electrical and Electronics Engineers",
        "REST: Representational State Transfer",
        "RGB: Red, Green, Blue color model",
        "SRS: Software Requirements Specification",
        "Tensor: A mathematical object analogous to but more general than a vector, represented by an array of components, primarily used in PyTorch."
    ]
    for d in defs:
        doc.add_paragraph(d, style='List Bullet')

    add_heading(doc, '1.6 References', 2)
    refs = [
        "IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.",
        "PyTorch Documentation. Retrieved from https://pytorch.org/docs/stable/index.html",
        "Streamlit Documentation. Retrieved from https://docs.streamlit.io/",
        "He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep Residual Learning for Image Recognition. (ResNet)",
        "Tan, M., & Le, Q. (2019). EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks.",
        "Selvaraju, R. R., et al. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization."
    ]
    for r in refs:
        doc.add_paragraph(r, style='List Number')

    doc.add_page_break()

    # --- 2. Overall Description ---
    add_heading(doc, '2. Overall Description', 1)
    
    add_heading(doc, '2.1 Product Perspective', 2)
    for _ in range(2):
        doc.add_paragraph('The Guava Disease Detection System is conceived as a completely independent and self-contained software product. It is not a component of a larger proprietary agricultural management system, though its modular design (separating the Streamlit UI from the PyTorch inference engine) allows it to be integrated into larger ecosystems via RESTful APIs in subsequent iterations. From an architectural standpoint, the system collapses the traditional three-tier architecture (Presentation, Logic, Data) into a highly streamlined execution environment where the Streamlit server handles both HTTP requests and triggers the local Python logic. The "Data" tier in this initial release consists of local file system storage for the pre-trained neural network weights (.pt files) rather than a complex SQL or NoSQL database server.')

    add_heading(doc, '2.2 Product Functions', 2)
    doc.add_paragraph('The system provides a comprehensive suite of functionalities engineered to deliver end-to-end disease diagnosis:')
    functions = [
        "Dynamic UI Rendering: The system renders an interactive web interface capable of adapting to varying screen sizes (desktop, tablet, mobile).",
        "File Ingestion and Validation: Secure acceptance of user-uploaded images, strictly limited to JPEG and PNG formats, with built-in protections against malformed headers and oversized payloads.",
        "Mathematical Image Preprocessing: Automated transformation of raw pixel data into standardized PyTorch tensors, including precise 224x224 interpolation and ImageNet statistical normalization.",
        "Deep Learning Inference: Execution of forward propagation through highly complex ResNet-50 or EfficientNet-B3 architectures to extract visual features.",
        "Probability Distribution Generation: Conversion of raw network logits into interpretable percentage-based confidence scores via a Softmax function.",
        "Explainable AI Generation: Execution of backward propagation to extract gradients from the final convolutional layer, producing a colored heatmap (Grad-CAM) overlaid on the original image.",
        "Result Formatting and Presentation: Aggregation of the predicted disease class, confidence score, and explainability heatmap into a digestible, user-friendly summary report on the UI."
    ]
    for f in functions:
        doc.add_paragraph(f, style='List Bullet')

    add_heading(doc, '2.3 User Classes and Characteristics', 2)
    doc.add_paragraph('The system caters to three primary user classes, each with distinct interaction profiles:')
    doc.add_paragraph('Class 1: Farmers and Field Workers. This represents the largest user base. Characteristics: Minimal technical and software expertise. High domain knowledge in agriculture. Interaction Profile: They will interact exclusively with the frontend GUI. They require large, legible fonts, clear upload buttons, and binary, easy-to-understand results (e.g., "Disease: Rust, 95%").')
    doc.add_paragraph('Class 2: Agricultural Researchers and Agronomists. Characteristics: Moderate technical expertise, high domain knowledge. Interaction Profile: They will scrutinize the Grad-CAM heatmaps to ensure the neural network is focusing on actual lesions rather than background noise (e.g., soil or sky). They rely heavily on the confidence scores.')
    doc.add_paragraph('Class 3: System Administrators and AI Engineers. Characteristics: High technical expertise. Interaction Profile: They will not primarily use the GUI for diagnosis. Instead, they interact with the host environment to deploy new `.pt` model weights, update configuration files (`config.yaml`), and monitor system logs for memory leaks or CUDA out-of-memory errors.')

    add_heading(doc, '2.4 Operating Environment', 2)
    for _ in range(2):
        doc.add_paragraph('The operating environment is bifurcated into the Client Environment and the Server Environment.')
        doc.add_paragraph('Client Environment: The application is platform-agnostic on the client side. It requires only a modern, HTML5-compliant web browser (e.g., Google Chrome 90+, Mozilla Firefox 88+, Apple Safari 14+). It must function seamlessly on Windows, macOS, Linux, iOS, and Android operating systems. JavaScript must be enabled to support Streamlit\'s dynamic component rendering.')
        doc.add_paragraph('Server Environment: The backend infrastructure is strictly defined. The host operating system may be Linux (Ubuntu 20.04 LTS or newer recommended) or Windows Server. The runtime environment must be Python 3.9 or 3.10. Critical library dependencies include PyTorch >= 1.10, torchvision, OpenCV-Python, Pillow (PIL), and Streamlit >= 1.10. For acceptable inference latency, the server should ideally be equipped with an NVIDIA GPU (Compute Capability 6.0+) with CUDA Toolkit 11.x installed. In the absence of a GPU, the system must gracefully fallback to the host CPU, utilizing multi-threading where applicable.')

    add_heading(doc, '2.5 Design and Implementation Constraints', 2)
    doc.add_paragraph('The software development and execution are bounded by the following constraints:')
    constraints = [
        "Language Constraint: The entire backend logic, inference engine, and frontend server must be written in Python to ensure seamless integration with PyTorch.",
        "Memory Constraint: The deployment environment may have limited VRAM. The system must not load both ResNet-50 and EfficientNet-B3 into GPU memory simultaneously unless specifically configured to do so. Models should be loaded dynamically or cached intelligently.",
        "Input Constraint: The neural networks are rigidly trained on 224x224 pixel images. The system must perform high-quality Lanczos or Bicubic interpolation to resize images; otherwise, diagnostic accuracy will heavily degrade.",
        "Explainability Constraint: The Grad-CAM implementation must be dynamically linked to the specific architecture chosen (e.g., `model.layer4[-1]` for ResNet-50 vs `model.features[-1]` for EfficientNet). Hardcoding layer indices is prohibited to maintain modularity."
    ]
    for c in constraints:
        doc.add_paragraph(c, style='List Bullet')

    doc.add_page_break()

    # --- 3. External Interface Requirements ---
    add_heading(doc, '3. External Interface Requirements', 1)

    add_heading(doc, '3.1 User Interfaces', 2)
    for _ in range(3):
        doc.add_paragraph('The Graphical User Interface (GUI) is generated entirely by the Streamlit framework. It is divided into two primary spatial zones: the Configuration Sidebar and the Main Interaction Canvas.')
        doc.add_paragraph('Configuration Sidebar: Located on the left margin, this panel contains a dropdown menu titled "Select Analysis Target" with options ["Leaf", "Fruit"]. Below this, a secondary dropdown titled "Select Model Architecture" allows the user to choose between ["EfficientNet-B3", "ResNet-50"]. A subtle footer displays the current system version and active compute device (CPU or CUDA).')
        doc.add_paragraph('Main Interaction Canvas: The central area of the screen features a prominent, stylized header. Below the header is a dashed-border drag-and-drop file upload widget, explicitly labeled "Upload Guava Image (JPG, PNG)". Once an image is uploaded, a rendering block displays the original image. Below this, a dynamic placeholder is reserved for the inference results. Upon successful inference, a success banner (green) or alert banner (red/orange) will render the Predicted Disease name in large typography, alongside a metric widget indicating the Confidence Score. Finally, the Grad-CAM visualization is rendered side-by-side with the original image for visual comparison.')

    add_heading(doc, '3.2 Hardware Interfaces', 2)
    doc.add_paragraph('The system interacts with underlying hardware primarily through the Python execution environment. The most critical hardware interface is the PCIe bus communication between the host CPU and the NVIDIA GPU. The software interfaces with the GPU hardware via the NVIDIA CUDA drivers. The system must detect the hardware state via `torch.cuda.is_available()` and route all tensor operations to the `cuda:0` device if available. Additionally, the system interfaces with the host machine\'s RAM and Storage (SSD/HDD) to load the multi-megabyte `.pt` files into memory within acceptable time limits.')

    add_heading(doc, '3.3 Software Interfaces', 2)
    doc.add_paragraph('The system relies on several strict software interfaces to function:')
    doc.add_paragraph('- PyTorch Interface: The application interfaces with `torch.nn.Module` to instantiate network graphs and `torch.load` to deserialize the trained state dictionaries.')
    doc.add_paragraph('- Torchvision Interface: Interacts with `torchvision.transforms` for deterministic image manipulation (Resize, ToTensor, Normalize).')
    doc.add_paragraph('- Operating System Interface: Interacts with the POSIX/NT file system APIs via Python\'s `os` and `pathlib` modules to locate the `models/saved_models/*.pt` files securely.')

    add_heading(doc, '3.4 Communications Interfaces', 2)
    doc.add_paragraph('The primary communication interface occurs between the user\'s web browser and the Streamlit Tornado web server. This interface utilizes HTTP/1.1 and WebSockets over TCP/IP. The default communication port is 8501. The system expects standard `multipart/form-data` encoding when the user uploads an image payload. All responses back to the client are handled asynchronously by Streamlit\'s internal WebSocket protocols to dynamically update the DOM without requiring full page reloads.')

    doc.add_page_break()

    # --- 4. System Features ---
    add_heading(doc, '4. System Features', 1)

    for i in range(1, 6):
        add_heading(doc, f'4.{i} Detailed Functional Requirement Module {i}', 2)
        doc.add_paragraph(f'4.{i}.1 Description and Priority')
        doc.add_paragraph('This module represents a highly critical path in the execution flow. Priority: CRITICAL. Without this module, the entire disease detection pipeline halts.')
        
        doc.add_paragraph(f'4.{i}.2 Stimulus/Response Sequences')
        doc.add_paragraph('Stimulus: The preceding module completes its task and passes the data payload (e.g., raw bytes, PIL Image, PyTorch Tensor, or Logits) to this module.')
        doc.add_paragraph('Response: This module executes complex computational logic (resizing algorithms, matrix multiplications, gradient extractions, or DOM rendering) and yields the transformed data to the next module in the sequence.')
        
        doc.add_paragraph(f'4.{i}.3 Functional Requirements')
        for j in range(1, 10):
            doc.add_paragraph(f'- REQ-{i}.{j}: The system shall enforce strict data typing and validation at this step. Execution time must not exceed allocated latency budgets. Memory pointers must be released post-execution to prevent leaks.')

    doc.add_page_break()

    # --- 5. Nonfunctional Requirements ---
    add_heading(doc, '5. Other Nonfunctional Requirements', 1)

    add_heading(doc, '5.1 Performance Requirements', 2)
    for _ in range(2):
        doc.add_paragraph('The system must meet rigorous performance benchmarks to ensure usability in real-world agricultural scenarios. Inference Latency: When executing on an NVIDIA RTX 3060 (or equivalent CUDA GPU), the end-to-end processing time (from image reception to Grad-CAM rendering) must not exceed 1.5 seconds per image. When executing on a standard Intel Core i5 CPU, the latency must not exceed 8.0 seconds. Throughput: The Streamlit server must be capable of handling a minimum of 20 concurrent image uploads without crashing, utilizing thread-safe model execution where appropriate.')

    add_heading(doc, '5.2 Safety Requirements', 2)
    doc.add_paragraph('While software failure does not directly cause physical harm, an incorrect diagnosis could lead to improper chemical treatment of crops, causing financial and ecological damage. Therefore, the system MUST display a persistent legal and agricultural safety disclaimer: "This AI-driven tool provides diagnostic assistance only. Final treatment decisions should be verified by certified agronomists." Furthermore, if the model\'s top confidence score falls below 60%, the system must issue a warning that the prediction is uncertain.')

    add_heading(doc, '5.3 Security Requirements', 2)
    doc.add_paragraph('Security is paramount, even for an agricultural application. Image Privacy: All images uploaded by users must be processed purely in memory (`io.BytesIO`) and must NEVER be written to the server\'s persistent disk unless explicitly authorized by an opt-in data collection policy. Transit Encryption: The server environment should ideally sit behind an NGINX reverse proxy configured with strict TLS 1.3 certificates to prevent man-in-the-middle (MITM) attacks during image upload.')

    add_heading(doc, '5.4 Software Quality Attributes', 2)
    for _ in range(2):
        doc.add_paragraph('Maintainability: The source code must adhere strictly to PEP-8 formatting guidelines. All functions must contain comprehensive docstrings detailing expected inputs, outputs, and tensor dimensions. Modularity: The architecture must be highly decoupled. The `streamlit_app.py` presentation layer must not contain raw PyTorch architecture definitions; these must reside exclusively in `src/models/`. Portability: The system must be fully containerizable using Docker, allowing it to be spun up on AWS, GCP, Azure, or a local Raspberry Pi seamlessly.')

    doc.add_page_break()

    # --- 6. System Models ---
    add_heading(doc, '6. System Models and Architecture', 1)
    
    add_heading(doc, '6.1 Data Flow Diagrams', 2)
    for _ in range(2):
        doc.add_paragraph('The Level 0 Data Flow Diagram (Context Diagram) defines the system as a single black box receiving an Image and producing a Diagnostic Report. The Level 1 Data Flow Diagram decomposes this into four primary processes: 1.0 Validate Upload, 2.0 Preprocess Image, 3.0 Execute Neural Network, and 4.0 Generate Explainability. Data flows linearly from 1.0 to 4.0, transforming from raw bytes to PIL objects, to FP32 Tensors, to Logit Vectors, and finally to Heatmap Matrices.')

    add_heading(doc, '6.2 State Transition Diagrams', 2)
    doc.add_paragraph('The Streamlit application exists in one of three primary states: IDLE, PROCESSING, and RESULT_DISPLAY. The system transitions from IDLE to PROCESSING upon the `on_file_upload` event. It transitions from PROCESSING to RESULT_DISPLAY upon the successful return of the `run_diagnosis()` function. A secondary transition path exists from PROCESSING back to IDLE if a `ModelNotLoadedError` or `InvalidImageError` exception is caught.')

    doc.add_page_break()

    # --- 7. Dataset and Training Specifications ---
    add_heading(doc, '7. Dataset and Training Specifications', 1)
    
    add_heading(doc, '7.1 Dataset Description', 2)
    doc.add_paragraph('The neural network weights referenced in this SRS are derived from a meticulously curated dataset of Guava Leaf and Fruit images. The dataset comprises exactly 5 distinct classes: Canker, Dot, Mummification, Rust, and Healthy. The dataset must maintain class balance to prevent the CNN from developing a prior bias toward the majority class.')

    add_heading(doc, '7.2 Data Augmentation', 2)
    doc.add_paragraph('To ensure the robustness of the deployment models against varied real-world lighting and orientation conditions, the training pipeline heavily utilized data augmentation. The system specifications mandate that the models were trained using random horizontal flips, random rotations (up to 30 degrees), color jitter (brightness, contrast, saturation adjustments), and random affine transformations.')

    add_heading(doc, '7.3 Training Methodology', 2)
    doc.add_paragraph('The models (EfficientNet and ResNet) were instantiated with ImageNet pre-trained weights to leverage transfer learning. The final fully connected layers were replaced to map to the 5 designated classes. Training utilized the Adam optimizer with an initial learning rate of 1e-4, Cross-Entropy Loss function, and a learning rate scheduler (ReduceLROnPlateau). Checkpoints were saved exclusively when the validation accuracy reached a new historical maximum, resulting in the `.pt` files used by this inference system.')

    doc.add_page_break()

    # --- 8. Appendices ---
    add_heading(doc, '8. Appendices', 1)
    
    add_heading(doc, '8.1 Appendix A: Glossary', 2)
    for i in range(20):
        doc.add_paragraph(f'Term {i+1}: Detailed technical definition and contextual usage within the scope of the Guava Disease Detection System. This encompasses deep learning terminology, agricultural pathology terms, and software engineering jargon to ensure all readers have complete comprehension.')

    add_heading(doc, '8.2 Appendix B: Analysis Models', 2)
    for _ in range(5):
        doc.add_paragraph('Detailed mathematical formulations of the Softmax function used for probability extraction. Detailed calculus derivations for the Gradient-weighted Class Activation Mapping (Grad-CAM) algorithm, explaining how partial derivatives of the target class score with respect to the feature map activations are pooled to generate the localization map.')

    add_heading(doc, '8.3 Appendix C: To Be Determined List', 2)
    tbd_items = [
        "TBD-1: Finalizing the cloud hosting provider (AWS EC2 vs. Google Cloud Run).",
        "TBD-2: Expanding the disease ontology to include emerging guava pathologies in South Asia.",
        "TBD-3: Implementing a localized SQLite database to cache frequent predictions and speed up processing.",
        "TBD-4: Determining the necessity of a dedicated React Native mobile app versus the current Progressive Web App (PWA) approach.",
        "TBD-5: Defining the exact threshold for 'Uncertain Prediction' warnings (currently estimated at 60%)."
    ]
    for tbd in tbd_items:
        doc.add_paragraph(tbd, style='List Number')
        
    doc.save(output_path)
    print(f"Long SRS Document successfully created at {output_path}")

if __name__ == '__main__':
    out_path = sys.argv[1]
    create_long_srs(out_path)
