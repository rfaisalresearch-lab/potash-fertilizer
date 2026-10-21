# Open this file in RStudio and click Source.
source_file <- tryCatch(sys.frame(1)$ofile, error=function(e) NULL)
project_dir <- if(!is.null(source_file)) dirname(normalizePath(source_file)) else getwd()
rm(source_file)
setwd(project_dir)
snakemake_bin <- Sys.which('snakemake')
if(!file.exists(snakemake_bin)) snakemake_bin <- Sys.which('snakemake')
if(file.exists(snakemake_bin)) {
 status <- system2(snakemake_bin, c('--cores','1','--printshellcmds'), stdout='snakemake_run.log', stderr='snakemake_run.log')
 if(status != 0) stop('Build failed. Read snakemake_run.log.')
} else {
 source('build.R')
 doc_python <- Sys.which('python3')
 if(!file.exists(doc_python)) doc_python <- Sys.which('python3')
 if(system2(doc_python, shQuote('build_explanation.py')) != 0) stop('Explanation build failed')
 if(system2(doc_python, shQuote('build_code_pdf.py')) != 0) stop('Code PDF build failed')
 if(system2(doc_python, shQuote('build_rights.py')) != 0) stop('Rights PDF build failed')
}
# Load the drawing functions for preview without rebuilding the exported files.
load_only <- TRUE
source('build.R')
rm(load_only)
if(requireNamespace('png',quietly=TRUE)) {
 grid::grid.newpage()
 grid::grid.raster(png::readPNG(file.path(project_dir,'Potash_Infographic.png')))
} else infographic()
if(requireNamespace('rstudioapi',quietly=TRUE)) rstudioapi::navigateToFile(file.path(project_dir,'build.R'))
cat('RStudio build complete. Files saved in:',project_dir,'\n')
