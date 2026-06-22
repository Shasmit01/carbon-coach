/**
 * Home page
 */
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary via-secondary to-accent">
      {/* Navigation */}
      <nav className="bg-primary bg-opacity-90 backdrop-blur-md text-white p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="text-2xl font-bold">🌍 Carbon Coach</div>
          <div className="space-x-4">
            <Link to="/login" className="px-4 py-2 rounded-lg hover:bg-secondary transition">
              Login
            </Link>
            <Link to="/register" className="px-4 py-2 bg-accent text-primary rounded-lg hover:bg-opacity-90 transition">
              Register
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-7xl mx-auto px-4 py-20 text-center text-white"
      >
        <h1 className="text-5xl font-bold mb-4">
          Track Your Carbon Footprint
        </h1>
        <p className="text-xl mb-8 text-gray-100">
          Get personalized recommendations to reduce your environmental impact with AI guidance
        </p>

        <Link
          to="/register"
          className="inline-block px-8 py-4 bg-accent text-primary font-bold rounded-lg hover:bg-opacity-90 transition text-lg"
        >
          Get Started Free
        </Link>
      </motion.div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: '📊',
              title: 'Track Activities',
              description: 'Monitor your daily activities and their carbon impact',
            },
            {
              icon: '🤖',
              title: 'AI Chatbot',
              description: 'Get personalized eco-friendly recommendations',
            },
            {
              icon: '🎯',
              title: 'Set Goals',
              description: 'Create and achieve carbon reduction goals',
            },
          ].map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="bg-white bg-opacity-10 backdrop-blur-md p-8 rounded-xl text-white"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p>{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Cost Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.6 }}
        className="text-center text-white py-20"
      >
        <h2 className="text-3xl font-bold mb-4">100% FREE Forever</h2>
        <p className="text-xl">No credit card. No hidden fees. Completely open source.</p>
      </motion.div>
    </div>
  );
}
