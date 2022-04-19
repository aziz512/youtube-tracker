const shell = require('shelljs');
const os = require('os');

shell.cd('../server');
if (os.platform() === 'linux') {
    shell.exec('make run', { async: true });
} else {
    shell.exec('flask run', { async: true });
}
shell.cd('../client');
shell.exec('npm start', { async: true });