require 'font-awesome-sass'
require 'bootstrap-sass'

# Set this to the root of your project when deployed:
http_path = "/"
css_dir = "css"
sass_dir = "sass"
images_dir = "images"
fonts_dir = "fonts"
#javascripts_dir = "js"
relative_assets = true

output_style = :compressed
environment = :production

if environment != :production
    sass_options = {:debug_info => true}
end

color_output = false