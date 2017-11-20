import os
import re
from shutil import copyfile
from urllib.parse import quote
import zipfile

from django.conf import settings

from .comicapi.comicarchive import ComicArchive

from . import utils


class ComicFileHandler(object):

    def __init__(self, file):
        self.file = file

    def extract_comic(self, cvid):
        '''
        Extract all the pages from a comic book file.

        Returns a dictionary containing the mediaurl and a list of files.
        '''
        ca = ComicArchive(self.file)
        mediaroot = settings.MEDIA_ROOT + '/temp/'
        mediaurl = settings.MEDIA_URL + 'temp/' + str(cvid) + '/'
        temppath = mediaroot + str(cvid)

        # File validation
        if ca.seemsToBeAComicArchive():
            # If directory already exists, return it.
            # Otherwise, create the directory.
            if os.path.isdir(temppath):
                if not os.listdir(temppath) == []:
                    pages = self._get_file_list(temppath)
                    return {'mediaurl': mediaurl, 'pages': pages}
            else:
                os.mkdir(temppath)

            if ca.isZip():
                extractor = self.get_extractor(self.file)
                image_list = ca.getPageNameList()
                for img in image_list:
                    extractor.extract(img, path=temppath)
                extractor.close()
            elif ca.isPdf():
                utils.extract_images_from_PDF(self.file, temppath)
            else:
                # I think it's alright to return None. Probably need to verify
                return None

            # Get a list of pages
            pages = self._get_file_list(temppath)

            for root, dirs, files in os.walk(temppath):
                for file in files:
                    if utils.valid_image_file(file):
                        image_path = root + '/' + file
                        utils.optimize_image(image_path, 75, 1920)

        return {'mediaurl': mediaurl, 'pages': pages}

    #=========================================================================

    def extract_cover(self):
        '''
        Extract the cover image from a comic file.

        Returns a path to the cover image.
        '''
        ca = ComicArchive(self.file)
        mediaroot = settings.MEDIA_ROOT + '/images/'
        mediaurl = 'media/images/'
        cover = ''

        # File validation
        if ca.seemsToBeAComicArchive():
            if ca.isZip():
                # Get extractor
                extractor = self.get_extractor(self.file)

                # Get cover file name
                first_image = self._get_first_image(extractor.namelist())
                normalised_file = self._normalise_image_name(first_image)
                cover_filename = os.path.splitext(normalised_file)[
                    0] + '-' + os.path.splitext(self.file)[0] + os.path.splitext(normalised_file)[1]

                # Delete existing cover if it exists
                self._delete_existing_cover(mediaroot + cover_filename)

                # Extract, rename, and optimize cover image
                extractor.extract(first_image, path=mediaroot)
                os.rename(mediaroot + first_image, mediaroot + cover_filename)
                cover = mediaurl + cover_filename

                # Close out zip extractor
                extractor.close()
            elif ca.isPdf():
                cover = utils.extract_first_image_from_PDF(self.file, mediaroot)
                cover = mediaurl + cover
            else:
                return None

            # Optimize cover image
            utils.optimize_image(cover, 75, 540)

        return cover

    #=========================================================================

    def get_page_count(self):
        page_count = 0

        ca = ComicArchive(self.file)
        filename = os.path.basename(self.file)
        mediaroot = settings.MEDIA_ROOT + '/images/'
        tempfile = mediaroot + filename

        # File validation
        if ca.seemsToBeAComicArchive():
            # Copy file to temp directory
            copyfile(self.file, tempfile)
            os.chmod(tempfile, 0o777)

            if ca.isZip():
                # Change extension if needed
                comic_file = self.normalise_comic_extension(tempfile)

                # Get extractor
                extractor = self.get_extractor(comic_file)

                for file in extractor.infolist():
                    if utils.valid_image_file(file.filename):
                        page_count += 1

                # Close out zip extractor
                extractor.close()
            if ca.isPdf():
                page_count = utils.get_PDF_page_count(self.file)
            else:
                return  None

        # Delete the temp comic file
        if os.path.isfile(tempfile):
            os.remove(tempfile)
        elif os.path.isfile(comic_file):
            os.remove(comic_file)

        return page_count

    #=========================================================================

    def _get_file_list(self, filepath):
        '''
        Returns a sorted list of image files for a comic. Filenames are changed
        to numbers so filepaths stay short.
        '''
        pages = []

        for root, dirs, files in os.walk(filepath):
            sorted_files = sorted(files)
            i = 0
            for file in sorted_files:
                if utils.valid_image_file(file):
                    file_ext = os.path.splitext(file)[1].lower()
                    path = os.path.join(root, file)
                    numbered_file = "%03d" % (i,) + file_ext
                    os.rename(path, filepath + '/' + numbered_file)
                    i += 1
                    newpath = numbered_file.replace(filepath + '/', '')
                    if os.name == 'nt':
                        newpath = numbered_file.replace(filepath + '\\', '')
                    pages.append(quote(newpath))

        return pages

    #=========================================================================

    def _get_first_image(self, filelist):
        ''' Returns the name of the first file from a sorted list. '''

        sorted_list = sorted(filelist)

        for file in sorted_list:
            if utils.valid_image_file(file):
                return file

    #=========================================================================

    def _delete_existing_cover(self, filepath):
        ''' Deletes cover image if found. '''

        if os.path.isfile(filepath):
            os.chmod(filepath, 0o777)
            os.remove(filepath)

    #=========================================================================

    def _normalise_image_name(self, filepath):
        '''	Returns a normalised image name. '''

        path_normalise = re.compile(r"[/\\]{1,}")
        filename = path_normalise.sub("`", filepath).split('`')[-1]
        return filename

    #=========================================================================

    def get_extractor(self, comic_file):
        ''' Return extractor based on file extension '''
        ca = ComicArchive(comic_file)

        if ca.isZip():
            e = zipfile.ZipFile(comic_file)

        return e
