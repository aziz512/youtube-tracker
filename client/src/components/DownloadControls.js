import { HOST } from '../common';
import { DOWNLOADED, DOWNLOADING, NOT_DOWNLOADING } from './Home';
import styled from 'styled-components';

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
        break;
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
