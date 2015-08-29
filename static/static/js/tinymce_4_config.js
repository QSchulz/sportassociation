// TinyMCE 4 configuration
// Modify the following code to customize TinyMCE
//Taken from: https://github.com/xyres/django-tinymce-noapp

tinymce.init({
	selector: "textarea",
	// Only required plugins are included. However, you can add more as per your needs.
	// Spellchecker plugin is excluded as it produces an error in version 4.x
	plugins: [
			"advlist autolink link image lists charmap preview hr",
			"searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media",
			"table contextmenu emoticons textcolor"
	],

	// Customize the toolbars below. You can also add new ones.
	toolbar1: "bold italic underline strikethrough | blockquote | bullist numlist | subscript superscript | table | hr | formatselect fontselect fontsizeselect",
	toolbar2: "undo redo | forecolor backcolor | link unlink | image media | alignleft aligncenter alignright alignjustify | outdent indent | charmap emoticons | searchreplace | removeformat code | preview fullscreen",
	// toolbar3: " add buttons here ",

	// Aditional options. Customize them as per your needs.
	height: 350,
	resize: "both",
	image_advtab: true,
	toolbar_items_size: "medium",
	menubar: true,

	// Example content CSS (should be your site CSS) for better typography
	content_css : "/static/css/style.css"
	// If your stylesheet is inside `static/css/` directory, just replace
	// `style.css` with your stylesheet's name. You don't need to change the path.
});
