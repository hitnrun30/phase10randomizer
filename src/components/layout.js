import PropTypes from "prop-types";
import React from "react";

// import Header from "./header";

function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen font-sans text-gray-900 bg-gradient-to-b from-blue-400 to-blue-700">

      <main className="flex-auto w-full max-w-4xl px-4 py-8 mx-auto md:px-8 md:py-16">
        {children}
      </main>

      <footer>
        <nav className="flex justify-between max-w-4xl p-4 mx-auto text-sm md:p-8">
          <p className="text-white">
            Created by{` `}
            <a
              className="font-bold no-underline"
              href="https://chis.dev"
              target="_blank"
              rel="noopener noreferrer"
            >
              Chris Alves
            </a>
          </p>

          <p>
            <a
              className="font-bold text-white no-underline"
              href="https://github.com/chrisae9"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
          </p>
        </nav>
      </footer>
    </div>
  );
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
};

export default Layout;
