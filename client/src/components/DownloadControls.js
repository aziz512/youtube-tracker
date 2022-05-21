import { HOST } from '../common';
import styled from 'styled-components';

export const DOWNLOADED = 'downloaded';
export const DOWNLOADING = 'downloading';
export const NOT_DOWNLOADING = 'not_found';

const DownloadControls = ({ video: { download_status, id }, onDownload }) => {
  const getControlsByStatus = (status) => {
    switch (status) {
      case DOWNLOADED:
        return (
          <>
            <a href={`${HOST}/downloads/${id}.mp4`} target="_blank">
              <ActionIcon src="play.png" alt="play icon" />
            </a>
          </>
        );
      case DOWNLOADING:
        return (
          <ButtonWrapper>
            <ActionIcon src="loading.png" alt="loading icon" />
          </ButtonWrapper>
        );
        break;
      case NOT_DOWNLOADING:
        return (
          <ButtonWrapper>
            <ActionIcon
              src="download.png"
              alt="download icon"
              onClick={() => onDownload()}
            />
          </ButtonWrapper>
        );
        break;
      default:
        return <></>;
    }
  };

  return <div>{getControlsByStatus(download_status)}</div>;
};

export default DownloadControls;

const ActionIcon = styled.img`
  width: 27px;
  margin: 5px auto;
  display: block;
`;

const ButtonWrapper = styled.button`
  margin: 0 auto;
  display: block;
  background: none;
  border: none;
  cursor: pointer;
`;
