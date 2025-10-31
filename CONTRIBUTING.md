# Contributing to Data Extraction Tools

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

1. **Fork the repository**

   ```bash
   git clone https://github.com/rahalio/data-extraction.git
   cd data-extraction
   ```

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Run tests**
   ```bash
   python -m unittest discover tests/
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Documentation

- Update README.md if you add new features
- Add docstrings with type hints
- Include usage examples for new functionality

### Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage

## 🔧 Adding New Features

### Adding a New Converter

1. Create a new file in `src/converters/`
2. Follow the existing converter patterns
3. Add appropriate error handling
4. Update `src/converters/__init__.py`
5. Add tests in `tests/`
6. Update README.md with usage examples

### Adding a New Combiner

1. Create a new file in `src/combiners/`
2. Follow the existing combiner patterns
3. Add appropriate error handling
4. Update `src/combiners/__init__.py`
5. Add tests in `tests/`
6. Update README.md with usage examples

## 📦 Pull Request Process

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Write clean, documented code
   - Add tests
   - Update documentation

3. **Test your changes**

   ```bash
   python -m unittest discover tests/
   ```

4. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Ensure CI tests pass

## 🐛 Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

## 💡 Feature Requests

We welcome feature requests! Please:

- Check if the feature already exists
- Provide a clear use case
- Explain why it would be useful
- Consider submitting a PR

## 📋 Code Review Process

- All submissions require review
- Maintainers will review PRs as time permits
- Address feedback promptly
- Keep PRs focused and manageable

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!
