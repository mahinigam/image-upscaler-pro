import React from 'react';
import { motion } from 'framer-motion';
import type { HTMLMotionProps } from 'framer-motion';
import clsx from 'clsx';
import { Sparkles, Loader2 } from 'lucide-react';

interface LiquidButtonProps extends HTMLMotionProps<"button"> {
    isLoading?: boolean;
    children: React.ReactNode;
}

export const LiquidButton: React.FC<LiquidButtonProps> = ({ children, isLoading, className, ...props }) => {
    return (
        <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={isLoading}
            className={clsx(
                "relative w-full py-5 px-8 overflow-hidden rounded-md group font-heading font-bold uppercase tracking-[0.15em] text-lg",
                "bg-gradient-to-r from-[#1a1a20] to-[#2a2a35] border border-white/10", // Base gradient
                "hover:text-black hover:border-transparent transition-colors duration-300",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                className
            )}
            {...props}
        >
            {/* Liquid Background on Hover */}
            <motion.div
                className="absolute inset-0 bg-neon-cyan"
                initial={{ x: '-100%' }}
                whileHover={{ x: '0%' }}
                transition={{ type: 'tween', ease: 'circOut', duration: 0.4 }}
            />

            <div className="relative flex items-center justify-center gap-3 z-10 w-full group-hover:text-black text-neon-cyan">
                {isLoading ? (
                    <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        <span>Processing...</span>
                    </>
                ) : (
                    <>
                        <Sparkles className="w-5 h-5" />
                        <span>{children}</span>
                    </>
                )}
            </div>

            {/* Glow effect */}
            <div className="absolute inset-0 rounded-md opacity-0 group-hover:opacity-100 shadow-[0_0_30px_rgba(102,252,241,0.4)] transition-opacity duration-300 pointer-events-none" />
        </motion.button>
    );
};
