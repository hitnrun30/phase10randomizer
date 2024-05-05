<!DOCTYPE html>
<html lang="en" data-react-helmet="lang" >
    <head>
        <title>Phase 10 Randomizer</title>
        <link rel="shortcut icon" href="./images//phase10icon.png" />
        </head>
		<meta charset="utf-8">
		<meta http-equiv="x-ua-compatible" content="ie=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<style>
<?php include 'main.css'; ?>
</style>
    <body>
		<div >
			<div style="outline:none">
				<div class="flex flex-col min-h-screen font-sans text-gray-900 bg-gradient-to-b from-blue-400 to-blue-700">
					<main class="flex-auto w-full max-w-4xl px-4 py-8 mx-auto md:px-8 md:py-16">
						<section class="text-center">
							<div class>			
								<img class="block w-1/2 mx-auto mb-4" src="./images//phase10logo.png"></img>
								<div class="text-center-text p-4 self-center rounded-3x1 overflow-hidden shadow-md">
									<ol class="text-white font-medium">
									<?PHP
										echo shell_exec("python phase10logic.py");
									?>
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
					<footer>
					</footer>					
				</div>
			</div>
			<div style="position:absolute;top:0;width:1px;height:1px;padding:0;overflow:hidden;clip:rect(0, 0, 0, 0);white-space:nowrap;border:0" aria-live="assertive" aria-atomic="true"></div>
		</div>
    </body>
</html>