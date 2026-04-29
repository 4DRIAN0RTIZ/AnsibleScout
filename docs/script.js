// Ansible Scout - Landing Page Script

// ── i18n ──────────────────────────────────────────────────────────────────────

const translations = {
  en: {
    'nav.features':    'Features',
    'nav.installation':'Installation',
    'nav.usage':       'Usage',
    'nav.shortcuts':   'Shortcuts',
    'nav.examples':    'Examples',

    'hero.badge':         'Terminal TUI Tool',
    'hero.tagline':       'Scout and discover Ansible modules instantly with fuzzy search recommendations',
    'hero.cta_primary':   'Get Started',
    'hero.cta_secondary': 'See Features',
    'hero.stat_features': 'Features',
    'hero.stat_shortcuts':'Shortcuts',
    'hero.stat_themes':   'Themes',
    'hero.stat_ai':       'Semantic Search',

    'features.title': 'Features',
    'feature.fuzzy_search.title': 'Real-time Fuzzy Search',
    'feature.fuzzy_search.desc':  'Find Ansible modules instantly as you type with intelligent fuzzy search algorithms',
    'feature.vim_nav.title':      'Vim-style Navigation',
    'feature.vim_nav.desc':       'Navigate seamlessly with familiar Vim keybindings for maximum efficiency',
    'feature.split_panel.title':  'Split-panel Interface',
    'feature.split_panel.desc':   'View search results and module details side-by-side for better workflow',
    'feature.module_details.title':'Module Details',
    'feature.module_details.desc': 'Access comprehensive information including parameters and usage examples',
    'feature.quick_selection.title':'Quick Selection',
    'feature.quick_selection.desc': 'Jump directly to results using number keys (1-9) for lightning-fast access',
    'feature.themes.title': 'Multiple Themes',
    'feature.themes.desc':  'Choose from multiple color themes including Original and Dracula',
    'feature.ai_search.title': 'AI Semantic Search',
    'feature.ai_search.desc':  'Press Ctrl+I for intelligent semantic search using OpenAI embeddings. Finds modules by meaning, not just text. Understands synonyms and context.',

    'installation.title': 'Installation',
    'installation.config': 'Configuration (Optional)',
    'installation.config_desc': 'Create ~/.config/ascout/config.toml for AI features:',
    'installation.curl':  'Using curl',
    'installation.wget':  'Or using wget',

    'usage.title':          'Usage',
    'usage.basic_mode':     'Basic Mode',
    'usage.custom_theme':   'With Custom Theme',
    'usage.custom_modules': 'Custom Modules File Location',

    'shortcuts.title':      'Keyboard Shortcuts',
    'shortcuts.navigation': 'Navigation (Vim-style)',
    'shortcuts.search':     'Search',
    'shortcuts.ai':         'AI Features',
    'shortcuts.selection':  'Selection',
    'shortcuts.general':    'General',

    'shortcut.move_down':   'Move down in results / scroll down in details',
    'shortcut.move_up':     'Move up in results / scroll up in details',
    'shortcut.jump_first':  'Jump to first result or top of details',
    'shortcut.jump_last':   'Jump to last result or bottom of details',
    'shortcut.scroll_down': 'Scroll details down one page',
    'shortcut.scroll_up':   'Scroll details up one page',
    'shortcut.focus_search':'Focus search input',
    'shortcut.clear_search':'Clear search',
    'shortcut.jump_number': 'Jump directly to result by number',
    'shortcut.show_details':'Show module details',
    'shortcut.cycle_focus': 'Cycle focus between search, results, and details',
    'shortcut.show_help':   'Show help screen',
    'shortcut.quit':        'Quit application',
    'shortcut.switch_theme':'Switch theme',
    'shortcut.ai_search':   'Semantic AI search with embeddings (Ctrl+I)',

    'examples.title':             'Examples',
    'examples.ai_search.title':   'AI Semantic Search',
    'examples.ai_search.step1':   'Type "backup database" in the search box',
    'examples.ai_search.step2':   'Press <kbd class="key">Ctrl</kbd> + <kbd class="key">I</kbd> to activate AI semantic search',
    'examples.ai_search.step3':   'AI finds semantically related modules: mysql_db, postgresql_db, archive',
    'examples.ai_search.step4':   'View AI recommendations and select the best module for your use case',
    'examples.copy_files.title':  'Search for file copying modules',
    'examples.copy_files.step1':  'Type "copy files" in the search box',
    'examples.copy_files.step2':  'Press <kbd class="key">1</kbd> to jump to the first result',
    'examples.copy_files.step3':  'Use <kbd class="key">j</kbd> / <kbd class="key">k</kbd> to browse other results',
    'examples.copy_files.step4':  'Press <kbd class="key">Enter</kbd> or <kbd class="key">d</kbd> to view details',
    'examples.quick_nav.title':   'Quick navigation',
    'examples.quick_nav.step1':   'Type your search query',
    'examples.quick_nav.step2':   'Press <kbd class="key">g</kbd> to jump to top result',
    'examples.quick_nav.step3':   'Press <kbd class="key">G</kbd> to jump to bottom result',
    'examples.quick_nav.step4':   'Press <kbd class="key">3</kbd> to jump directly to third result',

    'cta.title':  'Ready to Scout Ansible Modules?',
    'cta.desc':   'Install Ansible Scout and discover modules faster than ever before',
    'cta.button': 'Get Started',

    'footer.copy': '© 2026 Ansible Scout. Open source project for the Ansible community.',

    'copy.button': 'Copy',
    'copy.copied': 'Copied!',
  },

  es: {
    'nav.features':    'Funciones',
    'nav.installation':'Instalación',
    'nav.usage':       'Uso',
    'nav.shortcuts':   'Atajos',
    'nav.examples':    'Ejemplos',

    'hero.badge':         'Herramienta TUI de Terminal',
    'hero.tagline':       'Busca y descubre módulos de Ansible al instante con búsqueda difusa inteligente',
    'hero.cta_primary':   'Comenzar',
    'hero.cta_secondary': 'Ver funciones',
    'hero.stat_features': 'Funciones',
    'hero.stat_shortcuts':'Atajos',
    'hero.stat_themes':   'Temas',
    'hero.stat_ai':       'Búsqueda Semántica',

    'features.title': 'Funciones',
    'feature.fuzzy_search.title': 'Búsqueda difusa en tiempo real',
    'feature.fuzzy_search.desc':  'Encuentra módulos de Ansible al instante con algoritmos de búsqueda difusa inteligente',
    'feature.vim_nav.title':      'Navegación estilo Vim',
    'feature.vim_nav.desc':       'Navega con los atajos de teclado de Vim para máxima eficiencia',
    'feature.split_panel.title':  'Interfaz de panel dividido',
    'feature.split_panel.desc':   'Visualiza resultados y detalles del módulo en paralelo para mejor flujo de trabajo',
    'feature.module_details.title':'Detalles del módulo',
    'feature.module_details.desc': 'Accede a información completa incluyendo parámetros y ejemplos de uso',
    'feature.quick_selection.title':'Selección rápida',
    'feature.quick_selection.desc': 'Salta directamente a los resultados usando las teclas numéricas (1-9)',
    'feature.themes.title': 'Múltiples temas',
    'feature.themes.desc':  'Elige entre varios temas de color, incluyendo Original y Dracula',
    'feature.ai_search.title': 'Búsqueda Semántica con IA',
    'feature.ai_search.desc':  'Presiona Ctrl+I para búsqueda semántica inteligente usando embeddings de OpenAI. Encuentra módulos por significado, no solo texto. Entiende sinónimos y contexto.',

    'installation.title': 'Instalación',
    'installation.config': 'Configuración (Opcional)',
    'installation.config_desc': 'Crea ~/.config/ascout/config.toml para funciones de IA:',
    'installation.curl':  'Usando curl',
    'installation.wget':  'O usando wget',

    'usage.title':          'Uso',
    'usage.basic_mode':     'Modo básico',
    'usage.custom_theme':   'Con tema personalizado',
    'usage.custom_modules': 'Ubicación personalizada del archivo de módulos',

    'shortcuts.title':      'Atajos de teclado',
    'shortcuts.navigation': 'Navegación (estilo Vim)',
    'shortcuts.search':     'Búsqueda',
    'shortcuts.ai':         'Funciones de IA',
    'shortcuts.selection':  'Selección',
    'shortcuts.general':    'General',

    'shortcut.move_down':   'Bajar en resultados / desplazar detalles hacia abajo',
    'shortcut.move_up':     'Subir en resultados / desplazar detalles hacia arriba',
    'shortcut.jump_first':  'Ir al primer resultado o al inicio de detalles',
    'shortcut.jump_last':   'Ir al último resultado o al final de detalles',
    'shortcut.scroll_down': 'Desplazar detalles hacia abajo una página',
    'shortcut.scroll_up':   'Desplazar detalles hacia arriba una página',
    'shortcut.focus_search':'Enfocar campo de búsqueda',
    'shortcut.clear_search':'Limpiar búsqueda',
    'shortcut.jump_number': 'Saltar directamente al resultado por número',
    'shortcut.show_details':'Ver detalles del módulo',
    'shortcut.cycle_focus': 'Cambiar foco entre búsqueda, resultados y detalles',
    'shortcut.show_help':   'Mostrar pantalla de ayuda',
    'shortcut.quit':        'Salir de la aplicación',
    'shortcut.switch_theme':'Cambiar tema',
    'shortcut.ai_search':   'Búsqueda semántica con IA usando embeddings (Ctrl+I)',

    'examples.title':             'Ejemplos',
    'examples.ai_search.title':   'Búsqueda Semántica con IA',
    'examples.ai_search.step1':   'Escribe "backup database" en el campo de búsqueda',
    'examples.ai_search.step2':   'Presiona <kbd class="key">Ctrl</kbd> + <kbd class="key">I</kbd> para activar la búsqueda semántica con IA',
    'examples.ai_search.step3':   'La IA encuentra módulos relacionados semánticamente: mysql_db, postgresql_db, archive',
    'examples.ai_search.step4':   'Ve las recomendaciones de la IA y selecciona el mejor módulo para tu caso de uso',
    'examples.copy_files.title':  'Buscar módulos para copiar archivos',
    'examples.copy_files.step1':  'Escribe "copy files" en el campo de búsqueda',
    'examples.copy_files.step2':  'Presiona <kbd class="key">1</kbd> para saltar al primer resultado',
    'examples.copy_files.step3':  'Usa <kbd class="key">j</kbd> / <kbd class="key">k</kbd> para navegar otros resultados',
    'examples.copy_files.step4':  'Presiona <kbd class="key">Enter</kbd> o <kbd class="key">d</kbd> para ver detalles',
    'examples.quick_nav.title':   'Navegación rápida',
    'examples.quick_nav.step1':   'Escribe tu consulta de búsqueda',
    'examples.quick_nav.step2':   'Presiona <kbd class="key">g</kbd> para saltar al primer resultado',
    'examples.quick_nav.step3':   'Presiona <kbd class="key">G</kbd> para saltar al último resultado',
    'examples.quick_nav.step4':   'Presiona <kbd class="key">3</kbd> para saltar directamente al tercer resultado',

    'cta.title':  '¿Listo para explorar módulos de Ansible?',
    'cta.desc':   'Instala Ansible Scout y descubre módulos más rápido que nunca',
    'cta.button': 'Comenzar',

    'footer.copy': '© 2026 Ansible Scout. Proyecto de código abierto para la comunidad de Ansible.',

    'copy.button': 'Copiar',
    'copy.copied': '¡Copiado!',
  }
};

let currentLang = localStorage.getItem('lang') || 'en';

function t(key) {
  return translations[currentLang]?.[key] ?? translations.en[key] ?? key;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    el.innerHTML = t(el.dataset.i18nHtml);
  });
  document.documentElement.lang = currentLang;

  const langBtn = document.getElementById('langToggle');
  if (langBtn) langBtn.textContent = currentLang === 'en' ? 'ES' : 'EN';

  document.querySelectorAll('.copy-button:not(.copied)').forEach(btn => {
    btn.textContent = t('copy.button');
  });
}

// ── Boot ──────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  applyTranslations();
  initTheme();
  initNavbar();
  initSmoothScrolling();
  initScrollAnimations();
  initCodeCopy();
  initBackToTop();
});

// ── Theme ─────────────────────────────────────────────────────────────────────

function initTheme() {
  const saved = localStorage.getItem('theme');
  const theme = saved ?? (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  document.documentElement.setAttribute('data-theme', theme);
}

// ── Navbar ────────────────────────────────────────────────────────────────────

function initNavbar() {
  const navbar     = document.getElementById('navbar');
  const menuToggle = document.getElementById('menuToggle');
  const navLinks   = document.getElementById('navLinks');
  const langToggle = document.getElementById('langToggle');
  const themeToggle= document.getElementById('themeToggle');

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 10);
    updateActiveLink();
  }, { passive: true });

  menuToggle?.addEventListener('click', () => navLinks.classList.toggle('open'));

  navLinks?.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => navLinks.classList.remove('open'))
  );

  langToggle?.addEventListener('click', () => {
    currentLang = currentLang === 'en' ? 'es' : 'en';
    localStorage.setItem('lang', currentLang);
    applyTranslations();
  });

  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
}

function updateActiveLink() {
  const sections = document.querySelectorAll('section[id]');
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 80) current = s.id;
  });
  document.querySelectorAll('.nav-links a').forEach(a =>
    a.classList.toggle('active', a.getAttribute('href') === `#${current}`)
  );
}

// ── Smooth scroll ─────────────────────────────────────────────────────────────

function initSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
    });
  });
}

// ── Scroll animations ─────────────────────────────────────────────────────────

function initScrollAnimations() {
  const observer = new IntersectionObserver(
    entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      el.classList.add('animate-in');
      // Reset stagger delay after animation completes so hover transitions are instant
      const delay = parseFloat(el.style.transitionDelay || '0') * 1000;
      setTimeout(() => { el.style.transitionDelay = '0s'; }, 650 + delay);
      observer.unobserve(el);
    }),
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  // Stagger feature cards
  document.querySelectorAll('.feature-card').forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.06}s`;
    observer.observe(el);
  });

  document.querySelectorAll('.shortcuts-category, .code-block').forEach(el => {
    observer.observe(el);
  });
}

// ── Code copy ─────────────────────────────────────────────────────────────────

function initCodeCopy() {
  document.querySelectorAll('.code-block').forEach(block => {
    const btn = document.createElement('button');
    btn.className = 'copy-button';
    btn.textContent = t('copy.button');
    block.appendChild(btn);

    btn.addEventListener('click', async () => {
      const code = block.querySelector('code');
      if (!code) return;
      try {
        await navigator.clipboard.writeText(code.textContent.trim());
        btn.textContent = t('copy.copied');
        btn.classList.add('copied');
        setTimeout(() => {
          btn.textContent = t('copy.button');
          btn.classList.remove('copied');
        }, 2000);
      } catch { /* clipboard unavailable */ }
    });
  });
}

// ── Back to top ───────────────────────────────────────────────────────────────

function initBackToTop() {
  const btn = document.createElement('button');
  btn.className = 'back-to-top';
  btn.innerHTML = '↑';
  btn.setAttribute('aria-label', 'Back to top');
  document.body.appendChild(btn);

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 350);
  }, { passive: true });

  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}
