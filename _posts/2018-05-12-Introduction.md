---
layout: default
title: "Introduction"
date: 2018-05-12
---

<div class="text">
	<div class="container">
		<div class="header">
			<h2><a href="/">home</a> ~ <a href="/courses.html">courses</a> ~ <a href="/cubing/">cubing</a></h2>
		</div>
		<h1 style="text-align:left">Introduction</h1>
		<p>So you want to learn a bit about machine learning? I'm glad you're at the right place, because in the next few series of pages, I'll be teaching you the basics behind the mathematics and the inner working behind the field of "machine learning."</p>
		<h2>What is machine learning?</h2>
		<p>When people say "machine learning," we can't help to think about a robot sitting in a desk, and able to absorb information the same way humans do. This is not far from the intended definition of machine learning, although the image is slightly farfetched. </p>
		<p>Essentially, the crux of machine learning is to be able to make a computer program infer properties about data without being told explicitly what the values of these properties may be. The key is that we do not have to input specific rules into a machine learning model; the model will be able to guess these rules as it learns from the data.</p>
		<p><a href="http://www.cs.cmu.edu/~tom/">Tom Mitchell</a> gave the following formal definition of machine learning:</p>
		<blockquote style="padding-left:25px">
			<p>"A computer program is said to learn from experience \( E \) with respect to some class of tasks \( T \) and performance measure \( P \) if its performance at tasks in \( T \), as measured by \( P \), improves with experience \( E \)."</p>
		</blockquote>
		<p>Before digesting this definition, lets look at a few examples of machine learning models: </p>
		<hr>
		<p><b>Example 1.1: Spam Classification.</b> Have you ever wondered how Gmail or Hotmail or <i>*insert your favorite e-mail provider here*</i> automatically can filter spam emails for you? No need for spam to enter your inbox for you to figure it out manually; e-mail providers nowadays are able to filter these to a great degree of accuracy! A machine learning model was trained to look at body texts of e-mails (and perhaps some header information as well) in order to determine, for each one, if they are a spam e-mail or not. The key here is that we do not explicitly tell the model what specific words to look for, or specific phrases! Machine learning models do not have to be hardcoded this way, and can infer these features themselves!</p>
		<p><b>Example 1.2: Box Office Success.</b> Every week, hundreds of movies are flooded into the film industry, but only a few of them will make the cut and be deemed successful by the general public. What if we could predict a movie's success before it hits theaters? There are many measures of "success" for a movie, but one potential measure is how much a movie earns. We could build a machine learning model to take in several facts about a movie, including the name of the director, genre, and length, and predict the amount of money that the movie will make in theaters.</p>
		<hr>
		<p>Let's now break down the definition:</p>
		<h2>The Experience (\( E \))</h2>
		<p>In order for a model to accurately predict on new data, the model must first be exposed to pre-existing data that are similar in nature to the new data. We call the pre-existing data the <b>training data</b>, and the new data <b>test data</b>. Essentially, the training data provides a "learning experience" for a model, allowing it to learn rules from the old data.</p>
		<h2>The Tasks (\( T \))</h2>
		<p>The task is simply what the model is designed to do. There are two main tasks that are central to machine learning:</p>
		<h3>Classification</h3>
	</div>
</div>