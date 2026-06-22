/**
 * Not found page
 */
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center text-white"
      >
        <h1 className="text-6xl font-bold mb-4">404</h1>
        <p className="text-2xl mb-8">Page not found</p>
        <Link
          to="/"
          className="inline-block px-6 py-3 bg-accent text-primary font-bold rounded-lg hover:bg-opacity-90 transition"
        >
          Go Home
        </Link>
      </motion.div>
    </div>
  );
}
