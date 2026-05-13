/* soc-components.js — shared React components (plain createElement, no JSX)
 * Load after React + ReactDOM + Lucide, before any type="text/babel" script.
 * Usage: const { SocClock, Icon } = window.SocComponents;
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

    window.SocComponents = { SocClock, Icon };
})();
