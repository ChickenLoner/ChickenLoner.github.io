/* soc-components.js — shared React components (plain createElement, no JSX)
 * Load after React + ReactDOM + Lucide, before any type="text/babel" script.
 * Usage: const { SocClock, Icon, Section, Fig, resetFigCount, TipList, B, A, Code, CodeBlock, Img, dedent } = window.SocComponents;
 */
(function () {
    const SocClock = () => {
        const ref = React.useRef(null);
        React.useEffect(() => {
            const tick = () => {
                if (!ref.current) return;
                const n = new Date();
                ref.current.textContent = n.toISOString().slice(0, 10) + ' · ' + n.toISOString().slice(11, 19) + 'Z';
            };
            tick();
            const id = setInterval(tick, 1000);
            return () => clearInterval(id);
        }, []);
        return React.createElement('span', { ref, className: 'soc-clock' });
    };

    const Icon = ({ name, className = 'w-6 h-6', ...props }) => {
        const ref = React.useRef(null);
        React.useEffect(() => {
            if (!ref.current) return;
            const el = lucide[name] && lucide.createElement(lucide[name], { class: className });
            if (!el) return;
            ref.current.innerHTML = '';
            ref.current.appendChild(el);
        }, [name, className]);
        return React.createElement('i', { ref, className: `flex-shrink-0 ${className}`, ...props });
    };

    const dedent = (s) => {
        const lines = String(s).split('\n');
        const filled = lines.filter(l => l.trim().length > 0);
        if (!filled.length) return s;
        const firstIsUnindented = lines[0].trim().length > 0 && lines[0].match(/^[ \t]*/)[0].length === 0 && filled.length > 1;
        const forMin = firstIsUnindented ? filled.slice(1) : filled;
        const min = Math.min(...forMin.map(l => l.match(/^[ \t]*/)[0].length));
        return lines.map((l, i) => (i === 0 && firstIsUnindented) ? l : l.slice(min))
            .join('\n').replace(/^[\n\r]+|[\n\r]+$/g, '');
    };

    const CodeBlock = ({ language, children, prefix = 'res' }) =>
        React.createElement('div', { className: `${prefix}-code-wrap` },
            React.createElement('div', { className: `${prefix}-code-lang` }, language),
            React.createElement('div', { className: `${prefix}-code-body` },
                React.createElement('code', null, dedent(children))
            )
        );

    const Img = ({ src, alt, caption, prefix = 'res', base = '' }) =>
        React.createElement('figure', { className: `${prefix}-figure` },
            React.createElement('img', { src: `${base}/${src}`, alt: alt || '', loading: 'lazy' }),
            caption ? React.createElement('figcaption', null, caption) : null
        );

    let figCount = 0;
    const resetFigCount = () => { figCount = 0; };

    const Fig = ({ src, alt }) => {
        figCount += 1;
        const n = figCount;
        return React.createElement('figure', { className: 'my-5' },
            React.createElement('img', {
                src, alt: alt || `Figure ${n}`,
                className: 'rounded-xl border border-gray-200 shadow-sm max-w-full mx-auto block',
                loading: 'lazy'
            }),
            React.createElement('figcaption', { className: 'text-center text-xs text-gray-400 mt-1.5 font-mono' }, `Figure ${n}`)
        );
    };

    const TipList = ({ items }) =>
        React.createElement('ul', { className: 'list-disc list-outside ml-5 space-y-2 text-gray-700' },
            ...items.map((item, i) => React.createElement('li', { key: i }, item))
        );

    const B = ({ children }) => React.createElement('strong', null, children);

    const A = ({ href, children }) =>
        React.createElement('a', { href, target: '_blank', rel: 'noopener noreferrer', className: 'text-blue-600 hover:underline' }, children);

    const Code = ({ children }) =>
        React.createElement('code', { className: 'bg-gray-100 px-1.5 py-0.5 rounded text-sm font-mono' }, children);

    const Section = ({ id, title, icon, children }) =>
        React.createElement('section', { id, className: 'res-section' },
            React.createElement('div', { className: 'res-section-title' },
                React.createElement('div', { className: 'res-section-icon' },
                    React.createElement(Icon, { name: icon, className: 'w-4 h-4', style: { color: 'var(--soc-cy)' } })
                ),
                title
            ),
            React.createElement('div', { style: { display: 'flex', flexDirection: 'column', gap: '14px' } }, children)
        );

    const ThemeToggle = () =>
        React.createElement(
            'button',
            {
                className: 'soc-theme-btn',
                onClick: () => window.SocTheme && window.SocTheme.toggle(),
                type: 'button',
                'aria-label': 'Toggle theme'
            },
            React.createElement('span', { className: 'soc-tb-ico soc-tb-dark' }, '☀︎'),
            React.createElement('span', { className: 'soc-tb-ico soc-tb-light' }, '☽'),
            React.createElement('span', { className: 'soc-tb-track' },
                React.createElement('span', { className: 'soc-tb-knob' })
            ),
            React.createElement('span', { className: 'soc-tb-label' },
                React.createElement('span', { className: 'soc-tb-dark' }, 'LIGHT'),
                React.createElement('span', { className: 'soc-tb-light' }, 'DARK')
            )
        );

    window.SocComponents = { SocClock, Icon, ThemeToggle, dedent, CodeBlock, Img, Section, Fig, resetFigCount, TipList, B, A, Code };
})();
