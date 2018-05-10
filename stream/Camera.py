from threading import Condition
import picamera
import io

"""
camera.ISO - ISO get/set
camera.awb_mode - AWB Mode get/set https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera.PiCamera.awb_mode
"""

DEFAULT_RESOLUTION = '1280x720';
DEFAULT_FRAMERATE = 20;

class Camera:
    def __init__(self):
        self.camera = picamera.PiCamera(resolution=DEFAULT_RESOLUTION, framerate=DEFAULT_FRAMERATE);
        self.camera.rotation = 180;

        self.output = StreamingOutput()

        self.start();


    def start(self):
        self.camera.start_recording(self.output, format='mjpeg')
    
    def restart(self):
        self.camera.stop_recording();
        self.start();
    
    def close(self):
        self.camera.stop_recording()
        self.camera.close();

    def getState(self):
        return {
            'awb_mode': self.awb_mode(),
            'brightness': self.brightness(),
            'contrast': self.contrast(),
            'exposure_compensation': self.exposure_compensation(),
            'exposure_mode': self.exposure_mode(),
            #'framerate': self.framerate(),
            'hflip': self.hflip(),
            'image_effect': self.image_effect(),
            'iso': self.iso(),
            'meter_mode': self.meter_mode(),
            'resolution': self.resolution(),
            'rotation': self.rotation(),
            'saturation': self.saturation(),
            'sharpness': self.sharpness(),
            'vflip': self.vflip(),
            'video_stabilization': self.video_stabilization(),
            'zoom': self.zoom(),
        };

    # TODO: Individually test each of these
    def awb_mode(self, awb_mode = None):                           return self._getSetCameraProperty('awb_mode', awb_mode);
    def brightness(self, brightness = None):                       return self._getSetCameraProperty('brightness', brightness);
    def contrast(self, contrast = None):                           return self._getSetCameraProperty('contrast', contrast);
    def exposure_compensation(self, exposure_compensation = None): return self._getSetCameraProperty('exposure_compensation', exposure_compensation);
    def exposure_mode(self, exposure_mode = None):                 return self._getSetCameraProperty('exposure_mode', exposure_mode);
    # TODO: Return Fraction instance. Currently not serializable
    #def framerate(self, framerate = None):                         return self._getSetCameraProperty('framerate', framerate);
    def hflip(self, hflip = None):                                 return self._getSetCameraProperty('hflip', hflip);
    def image_effect(self, image_effect = None):                   return self._getSetCameraProperty('image_effect', image_effect);
    def iso(self, iso = None):                                     return self._getSetCameraProperty('iso', iso);
    def meter_mode(self, meter_mode = None):                       return self._getSetCameraProperty('meter_mode', meter_mode);
    def resolution(self, resolution = None):                       return self._getSetCameraProperty('resolution', resolution);
    def rotation(self, rotation = None):                           return self._getSetCameraProperty('rotation', rotation);
    def saturation(self, saturation = None):                       return self._getSetCameraProperty('saturation', saturation);
    def sharpness(self, sharpness = None):                         return self._getSetCameraProperty('sharpness', sharpness);
    def vflip(self, vflip = None):                                 return self._getSetCameraProperty('vflip', vflip);
    def video_stabilization(self, video_stabilization = None):     return self._getSetCameraProperty('video_stabilization', video_stabilization);
    # TODO: Uses tuple?
    def zoom(self, zoom = None):                                   return self._getSetCameraProperty('zoom', zoom);

    def _getSetCameraProperty(self, prop, value = None):
        if value:
            try: return setattr(self.camera, prop, value);
            except picamera.PiCameraValueError as error: return str(error);
        else: return getattr(self.camera, prop);

    # TODO: Handle different types
    def updateCamera(self, updates, restart = False):
        updateResults = {};
        for key in updates:
            try:
                updateFn = getattr(self, key);
                updateResults[key] = updateFn(updates[key]);
            except AttributeError: updateResults[key] = 'Invalid key' + key;

        if restart: self.restart();

        return updateResults;

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
