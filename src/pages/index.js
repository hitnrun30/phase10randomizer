import React from "react";

import Layout from "../components/layout";
import SEO from "../components/seo";
// import catAndHumanIllustration from "../images/cat-and-human-illustration.svg";
import phase10logo from "../images/phase10logo.png";
import phase10data from "../data/phase10data.json";

  var chosen = [];
  var selection = "";
  var phasenumbers = ["1","2","3","4","5","6","7","8","9","10"].sort(() => Math.random() - 0.5)

  phasenumbers.map(function(phase){
    while (true) {
      selection = phase10data[phase][Math.floor(Math.random() * phase10data[phase].length)];
      if (!chosen.includes(selection)) {
        chosen.push(selection)
        break;
      }
    }
  })

  function refreshPage() {
    window.location.reload(false);
  }

function phases() {
  return chosen.map(function (phase, index) {
    return (
      <li key={index}>
        {index + 1}){" "}
        {phase}
      </li>
    );
  });
}

function IndexPage() {
  return (
    <Layout>
      <SEO
        keywords={[`gatsby`, `tailwind`, `react`, `tailwindcss`]}
        title="Phase 10 Randomizer"
      />

      <section className="text-center">
        <div className="">
        <img
          alt="Cat and human sitting on a couch"
          className="block w-1/2 mx-auto mb-8"
          src={phase10logo}
        />
        <div className="p-4 self-center rounded-3x1 overflow-hidden shadow-md ">
          {/* <h2 className="inline-block p-3 mb-4 text-2xl font-bold bg-yellow-400">
          Randomizer
        </h2> */}
          <ul className="text-white font-medium">{phases()}</ul>
        </div>
        <div className="p-7">
          <button onClick={refreshPage} className="bg-yellow-400 hover:bg-yellow-300 text-black font-bold py-2 px-4 border border-blue-700 rounded">
            <a className="">Randomize</a>
          </button>
        </div>
        </div>
      </section>
    </Layout>
  );
}

export default IndexPage;
