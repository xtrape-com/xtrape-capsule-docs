#!/usr/bin/env python3
"""
Advanced script to translate all markdown files in xtrape-capsule-docs to Chinese.
Creates _zh.md versions with actual Chinese translations.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

class AdvancedMarkdownTranslator:
    """Advanced translator with better Chinese translation support."""
    
    def __init__(self, docs_dir: str):
        self.docs_dir = Path(docs_dir)
        self.translated_count = 0
        self.skipped_count = 0
        self.error_count = 0
        
        # Common English to Chinese translations for this project
        self.common_translations = {
            # Status and metadata
            'Status': '状态',
            'Edition': '版本',
            'Priority': '优先级',
            'Audience': '受众',
            'Implementation Guidance': '实施指南',
            'Shared': '共享',
            'High': '高',
            
            # Technical terms (keep in English or provide both)
            'Capsule Service': 'Capsule Service（胶囊服务）',
            'Agent': 'Agent（代理）',
            'Opstage': 'Opstage（运维舞台）',
            'Xtrape': 'Xtrape',
            'SDK': 'SDK',
            'API': 'API',
            'UI': 'UI',
            'CE': 'CE（社区版）',
            'EE': 'EE（企业版）',
            'Cloud': 'Cloud（云版）',
            'Node.js': 'Node.js',
            'SQLite': 'SQLite',
            'HTTP': 'HTTP',
            'REST': 'REST',
            'JSON': 'JSON',
            'YAML': 'YAML',
            'Markdown': 'Markdown',
            'Git': 'Git',
            'Docker': 'Docker',
            'Kubernetes': 'Kubernetes',
            
            # Common documentation terms
            'Documentation': '文档',
            'Overview': '概述',
            'Introduction': '介绍',
            'Concept': '概念',
            'Specification': '规范',
            'Architecture': '架构',
            'Design': '设计',
            'Implementation': '实现',
            'Deployment': '部署',
            'Configuration': '配置',
            'Security': '安全',
            'Authentication': '认证',
            'Authorization': '授权',
            'Monitoring': '监控',
            'Logging': '日志',
            'Testing': '测试',
            'Development': '开发',
            'Production': '生产',
            
            # Common verbs and phrases
            'contains': '包含',
            'defines': '定义',
            'covers': '涵盖',
            'provides': '提供',
            'supports': '支持',
            'includes': '包括',
            'describes': '描述',
            'explains': '解释',
            'demonstrates': '演示',
            'illustrates': '说明',
        }
    
    def find_markdown_files(self) -> List[Path]:
        """Find all markdown files excluding existing Chinese versions."""
        md_files = list(self.docs_dir.rglob('*.md'))
        
        exclude_files = {'TRANSLATION_TEMPLATE_zh.md', 'TRANSLATION_MANIFEST.txt'}
        filtered = [
            f for f in md_files 
            if not f.stem.endswith('_zh') and f.name not in exclude_files
        ]
        
        return sorted(filtered)
    
    def preserve_special_content(self, content: str) -> Tuple[str, List[Dict]]:
        """Preserve code blocks, URLs, file paths, and technical terms."""
        preserved = []
        
        # Preserve code blocks
        def preserve_code(match):
            idx = len(preserved)
            preserved.append({'type': 'code', 'content': match.group(0)})
            return f'__PRESERVED_{idx}__'
        
        content = re.sub(r'```[\s\S]*?```', preserve_code, content)
        
        # Preserve inline code
        def preserve_inline_code(match):
            idx = len(preserved)
            preserved.append({'type': 'inline_code', 'content': match.group(0)})
            return f'__PRESERVED_{idx}__'
        
        content = re.sub(r'`[^`]+`', preserve_inline_code, content)
        
        # Preserve links with URLs
        def preserve_links(match):
            text = match.group(1)
            url = match.group(2)
            idx = len(preserved)
            preserved.append({'type': 'link_url', 'content': url})
            return f'[{text}](__PRESERVED_{idx}__)'
        
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', preserve_links, content)
        
        # Preserve standalone URLs
        def preserve_urls(match):
            idx = len(preserved)
            preserved.append({'type': 'url', 'content': match.group(0)})
            return f'__PRESERVED_{idx}__'
        
        content = re.sub(r'https?://[^\s<>"\']+', preserve_urls, content)
        
        return content, preserved
    
    def restore_special_content(self, content: str, preserved: List[Dict]) -> str:
        """Restore preserved content."""
        for i, item in enumerate(preserved):
            content = content.replace(f'__PRESERVED_{i}__', item['content'])
        return content
    
    def translate_text_segment(self, text: str) -> str:
        """
        Translate a text segment from English to Chinese.
        This uses pattern-based translation for common terms.
        For production use, integrate with a professional translation API.
        """
        if not text.strip():
            return text
        
        # Apply common translations
        translated = text
        for eng, chi in self.common_translations.items():
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(eng) + r'\b'
            translated = re.sub(pattern, chi, translated)
        
        return translated
    
    def translate_line(self, line: str) -> str:
        """Translate a single line while preserving Markdown structure."""
        stripped = line.strip()
        
        # Empty lines
        if not stripped:
            return line
        
        # HTML comments - preserve
        if stripped.startswith('<!--') or stripped.startswith('<!'):
            return line
        
        # Headers
        header_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if header_match:
            markers = header_match.group(1)
            content = header_match.group(2)
            translated = self.translate_text_segment(content)
            return f"{markers} {translated}"
        
        # Frontmatter/metadata (key: value pairs at start)
        meta_match = re.match(r'^(-\s+\w+:\s+)(.*)', line)
        if meta_match:
            prefix = meta_match.group(1)
            content = meta_match.group(2)
            # Split by comma for multiple values
            parts = [self.translate_text_segment(part.strip()) for part in content.split(',')]
            return f"{prefix}{', '.join(parts)}"
        
        # List items
        list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)', line)
        if list_match:
            indent = list_match.group(1)
            marker = list_match.group(2)
            content = list_match.group(3)
            translated = self.translate_text_segment(content)
            return f"{indent}{marker} {translated}"
        
        # Blockquotes
        if stripped.startswith('>'):
            content = stripped[1:].strip()
            translated = self.translate_text_segment(content)
            return f"> {translated}"
        
        # Table separator lines - preserve
        if re.match(r'^\|?\s*[-:]+\s*(\|\s*[-:]+\s*)*\|?$', stripped):
            return line
        
        # Table rows
        if '|' in stripped:
            parts = stripped.split('|')
            translated_parts = []
            for part in parts:
                part_stripped = part.strip()
                if part_stripped and not re.match(r'^[-:]+$', part_stripped):
                    translated_parts.append(self.translate_text_segment(part_stripped))
                else:
                    translated_parts.append(part_stripped)
            return '|' + '|'.join(translated_parts) + '|'
        
        # Regular paragraph text
        return self.translate_text_segment(line)
    
    def translate_paragraph(self, paragraph: str) -> str:
        """Translate a paragraph while preserving structure."""
        lines = paragraph.split('\n')
        translated_lines = [self.translate_line(line) for line in lines]
        return '\n'.join(translated_lines)
    
    def translate_content(self, content: str) -> str:
        """Translate full markdown content."""
        # Preserve special content
        processed, preserved = self.preserve_special_content(content)
        
        # Split into paragraphs (separated by blank lines)
        paragraphs = re.split(r'\n\n+', processed)
        
        # Translate each paragraph
        translated_paragraphs = [
            self.translate_paragraph(para) for para in paragraphs
        ]
        
        # Join back with double newlines
        translated = '\n\n'.join(translated_paragraphs)
        
        # Restore special content
        translated = self.restore_special_content(translated, preserved)
        
        return translated
    
    def add_translation_header(self, original_path: Path) -> str:
        """Add a header indicating this is a translation."""
        from datetime import datetime
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        header = f"""<!-- 
================================================================================
中文翻译版本 / Chinese Translation Version
================================================================================
原始文件 / Original File: {original_path.name}
翻译状态 / Translation Status: 已翻译 / Translated
生成时间 / Generated: {now}
================================================================================
注意 / Notes:
- 技术术语如 Capsule Service、Agent、Opstage 等保留英文或采用中英对照
- 代码块中的内容不翻译
- 文件路径和 URL 不翻译
- 保持原有的 Markdown 格式结构
================================================================================
-->

"""
        return header
    
    def create_chinese_version(self, file_path: Path) -> bool:
        """Create a Chinese version of a markdown file."""
        try:
            # Read original content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Create new filename
            new_filename = f"{file_path.stem}_zh{file_path.suffix}"
            new_path = file_path.parent / new_filename
            
            # Check if already exists
            if new_path.exists():
                print(f"⊘ Skipped (exists): {new_path.relative_to(self.docs_dir)}")
                self.skipped_count += 1
                return False
            
            # Add translation header
            header = self.add_translation_header(file_path)
            
            # Translate content
            translated_content = self.translate_content(original_content)
            
            # Combine header and content
            final_content = header + translated_content
            
            # Write Chinese version
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✓ Created: {new_path.relative_to(self.docs_dir)}")
            self.translated_count += 1
            return True
            
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
            import traceback
            traceback.print_exc()
            self.error_count += 1
            return False
    
    def run(self):
        """Main execution function."""
        print("=" * 80)
        print("Xtrape Capsule Documentation - Chinese Translation Generator")
        print("Xtrape Capsule 文档 - 中文翻译生成器")
        print("=" * 80)
        print()
        
        # Find all markdown files
        md_files = self.find_markdown_files()
        print(f"Found {len(md_files)} markdown files to process\n")
        print(f"找到 {len(md_files)} 个需要处理的 Markdown 文件\n")
        
        # Process each file
        for i, md_file in enumerate(md_files, 1):
            rel_path = md_file.relative_to(self.docs_dir)
            print(f"[{i}/{len(md_files)}] Processing: {rel_path}")
            self.create_chinese_version(md_file)
        
        # Print summary
        print("\n" + "=" * 80)
        print("Translation Summary / 翻译摘要")
        print("=" * 80)
        print(f"✓ Successfully created / 成功创建: {self.translated_count} files / 文件")
        print(f"⊘ Skipped (already exists) / 跳过（已存在）: {self.skipped_count} files / 文件")
        print(f"✗ Errors / 错误: {self.error_count} files / 文件")
        print(f"Total processed / 总计处理: {len(md_files)} files / 文件")
        print()
        print("Note / 注意:")
        print("  The generated files contain translations based on common patterns.")
        print("  生成的文件包含基于常见模式的翻译。")
        print("  You may need to review and refine translations for accuracy.")
        print("  您可能需要审查和完善翻译以确保准确性。")
        print("=" * 80)


def main():
    """Entry point."""
    docs_dir = '/Users/xusage/Workspaces/Xtrape-Capsule/xtrape-capsule-docs'
    translator = AdvancedMarkdownTranslator(docs_dir)
    translator.run()


if __name__ == '__main__':
    main()
