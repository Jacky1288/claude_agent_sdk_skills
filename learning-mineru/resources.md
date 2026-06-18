# MinerU Resources

Comprehensive collection of links, tutorials, and references for learning MinerU.

## Official Resources

### Documentation

- **Official Documentation**: https://opendatalab.github.io/MinerU/
- **Quick Start Guide**: https://opendatalab.github.io/MinerU/quick_start/
- **Quick Usage Examples**: https://opendatalab.github.io/MinerU/usage/quick_usage/
- **CLI Tools Documentation**: https://opendatalab.github.io/MinerU/usage/cli_tools/
- **FAQ**: https://opendatalab.github.io/MinerU/faq/
- **Changelog**: https://opendatalab.github.io/MinerU/reference/changelog/
- **Docker Deployment**: https://opendatalab.github.io/MinerU/quick_start/docker_deployment/

### Code Repositories

- **Main Repository**: https://github.com/opendatalab/MinerU (67,500+ stars)
- **PyPI Package**: https://pypi.org/project/mineru/
- **HuggingFace Demo**: https://huggingface.co/spaces/opendatalab/MinerU
- **MinerU2.5-Pro Model**: https://huggingface.co/opendatalab/MinerU2.5-Pro-2604-1.2B
- **MinerU-HTML**: https://github.com/opendatalab/MinerU-HTML
- **MinerU-Diffusion**: https://github.com/opendatalab/MinerU-Diffusion

### API Resources

- **Official API Docs**: https://mineru.net/apiManage/docs
- **FastAPI Documentation**: Available at `http://127.0.0.1:8000/docs` when running `mineru-api`

## Community Tutorials

### Beginner-Friendly Guides

1. **MinerU Beginner's Guide** by StableLearn
   - URL: https://stable-learn.com/en/mineru-tutorial/
   - Coverage: Installation, multilingual support, optimization, troubleshooting
   - Best for: First-time users

2. **Extract Any PDF with MinerU 2.5** by Sonu Sahani
   - URL: https://sonusahani.com/blogs/mineru
   - Coverage: MinerU 2.5 with vLLM integration, practical testing
   - Best for: Understanding performance characteristics

3. **Official Quick Start**
   - URL: https://opendatalab.github.io/MinerU/quick_start/
   - Coverage: Basic commands, online demos
   - Best for: Quick overview before local deployment

### Video Tutorials

1. **MinerU 2.5 with vLLM: Extract Data from Any PDF - Easy Tutorial**
   - Platform: YouTube
   - URL: https://www.youtube.com/watch?v=xjC2_61ULe4
   - Coverage: Step-by-step installation and usage with vLLM

## Technical Deep Dives

### Research Papers

1. **MinerU: An Open-Source Solution for Precise Document Content Extraction**
   - URL: https://arxiv.org/abs/2409.18839
   - Published: September 2024
   - Focus: Comprehensive technical documentation

2. **MinerU2.5: A Decoupled Vision-Language Model for Efficient High-Resolution Document Parsing**
   - URL: https://arxiv.org/pdf/2509.22186
   - Focus: Architecture and performance improvements

3. **MinerU2.5-Pro: Pushing the Limits of Data-Centric Document Parsing at Scale**
   - URL: https://arxiv.org/pdf/2604.04771
   - Focus: Latest model improvements and benchmarks

4. **MinerU-Diffusion: Rethinking Document OCR as Inverse Rendering**
   - URL: https://arxiv.org/html/2603.22458v1
   - Focus: Novel OCR approach

### Technical Articles

1. **MinerU2.5 Vision-Language Model Explained** by Medium
   - URL: https://medium.com/@huguosuo/mineru2-5-a-decoupled-vision-language-model-for-efficient-high-resolution-document-parsing-5ac976ee679f
   - Best for: Understanding the architecture

2. **Stop Wasting Hours on PDF Parsing!** by BrightCoding
   - URL: https://www.blog.brightcoding.dev/2026/06/03/stop-wasting-hours-on-pdf-parsing-mineru-is-the-secret-weapon-top-ai-teams-use
   - Best for: Real-world use cases and ROI

## Comparison & Analysis

### Tool Comparisons

1. **Best Open Source PDF to Markdown Tools: Marker vs MinerU vs MarkItDown**
   - URL: https://jimmysong.io/blog/pdf-to-markdown-open-source-deep-dive/
   - Key insight: MinerU excels at formula recognition (90%+ BLEU) vs Marker (<70%)
   - Best for: Choosing the right tool for your use case

2. **12 Open-Source PDF Parsing & OCR Tools Evaluated**
   - URL: https://liduos.com/en/posts/ai-develope-tools-series-2-open-source-doucment-parsing
   - Coverage: Comparative analysis across multiple tools
   - Best for: Understanding MinerU's position in the ecosystem

3. **Self-Host Document Intelligence Guide**
   - URL: https://www.spheron.network/blog/self-host-document-intelligence-docling-marker-mineru-rag-guide/
   - Focus: Deployment considerations for RAG systems

### Benchmark Resources

- **DeepWiki Benchmarking**: https://deepwiki.com/loorr-fork/MinerU/5.3-benchmarking
- **OmniDocBench Results**: Referenced in official documentation and papers

## Community Support

### Discussion Forums

- **GitHub Discussions**: https://github.com/opendatalab/MinerU/discussions
  - General Q&A and support
  - Feature requests and feedback

- **GitHub Issues**: https://github.com/opendatalab/MinerU/issues
  - Bug reports (191+ open issues as of June 2026)
  - Technical troubleshooting

### Key Discussion Topics

- **Docker Deployment Issues**: https://github.com/opendatalab/MinerU/discussions/2961
- **PyTorch Compatibility**: https://github.com/opendatalab/MinerU/discussions/3337
- **vLLM Integration**: https://github.com/opendatalab/MinerU/discussions/3548

## Alternative Tools

For comparison and context:

- **Marker**: https://github.com/VikParuchuri/marker (faster, balanced approach)
- **MarkItDown**: https://github.com/microsoft/markitdown (broad format support)
- **30 Best MinerU Alternatives**: https://www.aitoolnet.com/alternative/mineru

## Common Gotchas & Troubleshooting

### Resource Issues

- **VRAM Requirements**: Complex documents can peak >25GB on 48GB GPU
- **Concurrency Problems**: Single instance = MAX_CONCURRENT_REQUESTS=1 recommended
- **Thread Safety**: "Corrupted double-linked list" errors under concurrent load

### Language Support

- **Strong**: English, Chinese
- **Unreliable**: Arabic, Hindi, Urdu (text extraction issues)
- **Mixed**: Indonesian (variable results)
- **Total Languages**: 109 supported via OCR

### Known Limitations

- No vertical text support
- Single-level heading support only
- Comic books/art albums not well-supported
- Complex nested tables may have errors
- 300-second (5-minute) processing timeout for large files

## Integration Resources

### Framework Integrations

- **LangChain**: Mentioned in official docs
- **Dify**: Supported integration
- **FastGPT**: Supported integration
- **MCP Server**: Available for AI agent integration

### SDKs & APIs

- **Python SDK**: Primary interface via `mineru` package
- **Go SDK**: Mentioned in documentation
- **TypeScript SDK**: Mentioned in documentation
- **REST API**: FastAPI-based with OpenAPI docs

## Advanced Topics

### Performance Optimization

- **Flash-MinerU**: Ray-based distributed processing
- **mineru-router**: Multi-GPU deployment and load balancing
- **Backend Selection**: Pipeline (CPU), VLM (GPU), Hybrid (balanced)

### Model Management

- **Model Hub**: HuggingFace model repository
- **Local Model Storage**: Configuration via `mineru.json`
- **vLLM Integration**: High-throughput inference
- **LMDeploy Support**: Alternative inference backend

## Industry Recognition

- **MarkTechPost**: https://www.marktechpost.com/2024/10/05/mineru-an-open-source-pdf-data-extraction-tool/
- **AIBase**: https://www.aibase.com/tool/34498
- **Emergent Mind**: https://www.emergentmind.com/topics/mineru-parser

## Version History

- **Latest**: 2.7.6 (February 6, 2026)
- **Major Release**: mineru-3.3.1 (June 11, 2026)
- **Model Version**: MinerU2.5-Pro-2604-1.2B

## Key Statistics

- **GitHub Stars**: 67,500+
- **Forks**: 5,300+
- **Performance**: 95.69% accuracy on OmniDocBench v1.6
- **Throughput**: ~1,800 pages/hour (mixed documents), 1,200-1,500 pages/hour (scientific papers)
- **Formula Recognition**: 90%+ BLEU score on displayed equations

---

**Last Updated**: June 2026

For the most current information, always check the [official documentation](https://opendatalab.github.io/MinerU/).
