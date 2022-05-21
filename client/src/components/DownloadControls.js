import { HOST } from '../common';
import { DOWNLOADED, DOWNLOADING, NOT_DOWNLOADING } from './Home';

const DownloadControls = ({ video: { download_status, id }, onDownload }) => {
  const getControlsByStatus = (status) => {
    switch (status) {
      case DOWNLOADED:
        return (
          <>
            <a href={`${HOST}/downloads/${id}.mp4`} target="_blank">
              <button>Play</button>
            </a>
          </>
        );
      case DOWNLOADING:
        return <>Downloading</>;
        break;
      case NOT_DOWNLOADING:
        return (
          <>
            <button onClick={() => onDownload()}>D</button>
          </>
        );
        break;
      default:
        break;
    }
  };

  return <div>{getControlsByStatus(download_status)}</div>;
};

export default DownloadControls;
