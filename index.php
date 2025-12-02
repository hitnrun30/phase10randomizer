<?php
require_once dirname(__DIR__) . '/python_client.php';

/**
 * Load current config from phase10config.json so the UI shows real values.
 */
$configPath = __DIR__ . '/phase10config.json';
$config = [];
if (is_readable($configPath)) {
    $json = file_get_contents($configPath);
    $cfg = json_decode($json, true);
    if (is_array($cfg)) {
        $config = $cfg;
    }
}

function cfg(array $cfg, string $key, $default) {
    return array_key_exists($key, $cfg) ? $cfg[$key] : $default;
}

/* --- Bind settings (GET overrides JSON, JSON overrides hard defaults) --- */

$use_mc = isset($_GET['use_mc'])
    ? $_GET['use_mc']
    : (cfg($config, 'USE_MONTE_CARLO', true) ? '1' : '0');

$show_prob = isset($_GET['show_prob'])
    ? $_GET['show_prob']
    : (cfg($config, 'SHOW_PHASE_PROBABILITY', true) ? '1' : '0');

$mc_trials = isset($_GET['mc_trials'])
    ? (int)$_GET['mc_trials']
    : (int)cfg($config, 'MC_TRIALS_DEFAULT', 5000);

$color_rand = isset($_GET['color_rand'])
    ? (int)$_GET['color_rand']
    : (int)cfg($config, 'COLOR_RAND', 8);

$wild_rand = isset($_GET['wild_rand'])
    ? (int)$_GET['wild_rand']
    : (int)cfg($config, 'WILD_RAND', 20);

$max_per_phase = isset($_GET['max_per_phase'])
    ? (int)$_GET['max_per_phase']
    : (int)cfg($config, 'TYPE_MAX_PER_PHASE', 2);

$min_cards = isset($_GET['min_cards'])
    ? (int)$_GET['min_cards']
    : (int)cfg($config, 'MIN_CARDS_PER_PHASE', 6);

$max_per_type = isset($_GET['max_per_type'])
    ? (int)$_GET['max_per_type']
    : (int)cfg($config, 'TYPE_MAX_PER_TYPE_GLOBAL', 2);

$html_timeout = isset($_GET['html_timeout'])
    ? (float)$_GET['html_timeout']
    : (float)cfg($config, 'HTML_TIMEOUT_SECONDS', 5);

/**
 * Call Python service and return the <li> list HTML.
 */
function get_phase10_html()
{
    global $html_timeout;

    $path = "/phase10/html";

    $qs = isset($_SERVER['QUERY_STRING']) ? $_SERVER['QUERY_STRING'] : '';
    if ($qs !== '') {
        $path .= '?' . $qs;
    }

    // php timeout slightly above HTML timeout
    $curlTimeout = max(1, (int)ceil($html_timeout + 1));

    // Tell the generic client which env var to consult for this project
    $html = callPython($path, $curlTimeout, 'PHASE10_BASE_URL');

    if ($html === null || $html === '') {
        return "<li>Error: could not load phases from Python service.</li>";
    }

    return $html;
}
?>
<!DOCTYPE html>
<html lang="en" data-react-helmet="lang" >
    <head>
        <title>Phase 10 Randomizer</title>
        <link rel="shortcut icon" href="./images//phase10icon.png" />
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <style>
<?php include 'main.css'; ?>
        </style>
    </head>
    <body>
        <div id="config-container">
            <button
                id="config-toggle"
                type="button"
                title="Settings"
            >
                &#9881;
            </button>

            <form
                id="config-panel"
                method="get"
                style="display:none;"
            >
                <!-- everything inside the form stays exactly as we already set up:
                    use_mc, mc_trials, show_prob, color_rand, wild_rand, etc. -->
                <!-- Use Monte Carlo -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium">Use Monte Carlo:</label><br>
                    <label class="text-sm mr-2">
                        <input type="radio" name="use_mc" value="1" <?php echo ($use_mc === '1') ? 'checked' : ''; ?>>
                        Yes
                    </label>
                    <label class="text-sm">
                        <input type="radio" name="use_mc" value="0" <?php echo ($use_mc === '0') ? 'checked' : ''; ?>>
                        No
                    </label>
                </div>

                <!-- MC Trials -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="mc_trials">MC Trials:</label><br>
                    <input
                        id="mc_trials"
                        name="mc_trials"
                        type="number"
                        min="100"
                        max="100000"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$mc_trials, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <!-- Show Probability -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium">Show Probability:</label><br>
                    <label class="text-sm mr-2">
                        <input type="radio" name="show_prob" value="1" <?php echo ($show_prob === '1') ? 'checked' : ''; ?>>
                        Yes
                    </label>
                    <label class="text-sm">
                        <input type="radio" name="show_prob" value="0" <?php echo ($show_prob === '0') ? 'checked' : ''; ?>>
                        No
                    </label>
                </div>

                <!-- COLOR_RAND -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="color_rand">Color randomness (COLOR_RAND):</label><br>
                    <input
                        id="color_rand"
                        name="color_rand"
                        type="number"
                        min="1"
                        max="100"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$color_rand, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <!-- WILD_RAND -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="wild_rand">Wild randomness (WILD_RAND):</label><br>
                    <input
                        id="wild_rand"
                        name="wild_rand"
                        type="number"
                        min="1"
                        max="100"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$wild_rand, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <!-- TYPE_MAX_PER_PHASE -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="max_per_phase">Max types per phase (TYPE_MAX_PER_PHASE):</label><br>
                    <input
                        id="max_per_phase"
                        name="max_per_phase"
                        type="number"
                        min="1"
                        max="10"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$max_per_phase, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <!-- MIN_CARDS_PER_PHASE -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="min_cards">Min cards per phase (MIN_CARDS_PER_PHASE):</label><br>
                    <input
                        id="min_cards"
                        name="min_cards"
                        type="number"
                        min="1"
                        max="10"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$min_cards, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <!-- TYPE_MAX_PER_TYPE_GLOBAL -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="max_per_type">Max per type globally (TYPE_MAX_PER_TYPE_GLOBAL):</label><br>
                    <input
                        id="max_per_type"
                        name="max_per_type"
                        type="number"
                        min="3"
                        max="20"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$max_per_type, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <!-- HTML_TIMEOUT_SECONDS -->
                <div class="mb-2">
                    <label class="text-sm text-white font-medium" for="html_timeout">HTML timeout seconds:</label><br>
                    <input
                        id="html_timeout"
                        name="html_timeout"
                        type="number"
                        step="0.1"
                        min="1"
                        max="30"
                        class="px-3 py-1 rounded text-black"
                        value="<?php echo htmlspecialchars((string)$html_timeout, ENT_QUOTES, 'UTF-8'); ?>"
                    >
                </div>

                <div class="mt-2">
                    <button
                        type="submit"
                        class="bg-yellow-400 hover:bg-yellow-300 text-black font-bold py-1 px-3 border border-blue-700 rounded"
                    >
                        Apply Settings
                    </button>
                </div>
            </form>
        </div>

        <div>
            <div style="outline:none">
                <div class="flex flex-col min-h-screen font-sans text-gray-900 bg-gradient-to-b from-blue-400 to-blue-700">
                    <main class="flex-auto w-full max-w-4xl px-4 py-8 mx-auto md:px-8 md:py-16">
                        <section class="text-center">
                            <div>            
                                <img class="block w-1/2 mx-auto mb-4" src="./images//phase10logo.png"></img>
                                <div class="text-center-text p-4 self-center rounded-3x1 overflow-hidden shadow-md">
                                    <ol class="text-white font-medium">
                                        <ul id="phases">
                                            <?= get_phase10_html() ?>
                                        </ul>
                                    </ol>
                                </div>
                                <div class="p-7">                                
                                    <button class="bg-yellow-400 hover:bg-yellow-300 text-black font-bold py-2 px-4 border border-blue-700 rounded" onClick="window.location.reload();">
                                        <a>Randomize</a>
                                    </button>
                                </div>
                            </div>
                        </section>
                    </main>
                    <footer></footer>                    
                </div>
            </div>
            <div style="position:absolute;top:0;width:1px;height:1px;padding:0;overflow:hidden;clip:rect(0, 0, 0, 0);white-space:nowrap;border:0" aria-live="assertive" aria-atomic="true"></div>
        </div>

        <script>
            (function () {
                var toggle = document.getElementById('config-toggle');
                var panel  = document.getElementById('config-panel');
                if (!toggle || !panel) return;

                toggle.addEventListener('click', function () {
                    if (panel.style.display === 'none' || panel.style.display === '') {
                        panel.style.display = 'block';
                    } else {
                        panel.style.display = 'none';
                    }
                });
            })();
        </script>
    </body>
</html>
